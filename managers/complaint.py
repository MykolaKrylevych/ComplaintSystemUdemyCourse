import os

from models import complaint, RoleType, State, transaction
from db import database
from services.s3 import S3Service
from services.ses import SESService
from constants import TEMP_FILE_FOLDER

from utils.helper import decode_photo

import uuid
from decouple import config
from services.wise import WiseService

s3 = S3Service()
ses = SESService()
wise = WiseService()


class ComplaintManager:
    @staticmethod
    async def get_complaints(user):
        q = complaint.select()
        if user["role"] == RoleType.complainer:
            q = q.where(complaint.c.complainer_id == user["id"])
        elif user["role"] == RoleType.approver:
            q = q.where(complaint.c.status == State.pending)
        return await database.fetch_all(q)

    @staticmethod
    async def create_complaint(complaint_data, user):
        complaint_data["complainer_id"] = user["id"]
        encoded_photo = complaint_data.pop("encoded_photo")
        extensions = complaint_data.pop("extension")
        name = f"{uuid.uuid4()}.{extensions}"
        path = os.path.join(TEMP_FILE_FOLDER, name)
        decode_photo(path, encoded_photo)
        complaint_data["photo_url"] = s3.upload(path, name, extensions)
        os.remove(path)
        async with database.transaction() as tconn:
            id_ = await tconn._connection.execute(complaint.insert().values(complaint_data))
            await ComplaintManager.issue_transactions(tconn, complaint_data["amount"],
                                                      f"{user['first_name']} {user['last_name']}",
                                                      user["iban"], id_)
        return await database.fetch_one(complaint.select().where(complaint.c.id == id_))

    @staticmethod
    async def delete(complaint_id):
        await database.execute(complaint.delete().where(complaint.c.id == complaint_id))

    @staticmethod
    async def approve(id_):
        await database.execute(
            complaint.update()
            .where(complaint.c.id == id_)
            .values(status=State.approved)
        )
        transactions_data = await database.fetch_one(transaction.select().where(transaction.c.complaint_id == id_))
        wise.fund_transfer(transactions_data["transfer_id"])
        ses.send_mail("Complaint approved!", [config("MY_EMAIL2")],
                      "Congrats! Your claim is approved, check your bank account in 2 days for your refund")

    @staticmethod
    async def reject(id_):
        transactions_data = await database.fetch_one(transaction.select().where(transaction.c.complaint_id == id_))
        wise.cancel_fund(transactions_data["transfer_id"])
        await database.execute(
            complaint.update()
            .where(complaint.c.id == id_)
            .values(status=State.rejected)
        )

    @staticmethod
    async def issue_transactions(tconn, amount, full_name, iban, complaint_id):

        quote_id = wise.create_quote(amount)
        recipient_id = wise.create_recipient_account(full_name, iban)
        transfer_id = wise.create_transfer(recipient_id, quote_id)
        data = {
            "quote_id": quote_id,
            "transfer_id": transfer_id,
            "target_account_id": str(recipient_id),
            "amount": amount,
            "complaint_id": complaint_id
        }
        await tconn._connection.execute(transaction.insert().values(**data))
