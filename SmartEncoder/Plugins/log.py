async def upload_log_file(client, message):
  if message.from_user.id in AUTH_USERS:
    await message.reply_document(
        LOG_FILE_ZZGEVC
    )
  else:
    return
