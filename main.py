from telegram.ext import Updater, MessageHandler, CallbackContext, Filters
from telegram import Update
from huggingface_hub import InferenceClient
import os

pid = os.getpid()
print(f"I am starting main.py file - {pid}")

# parameters
user_name_hugging_face = "borodache"
model_name_hugging_face = "distilBERT_toxic_detector_multi_label"
token_model = "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"

try:
    client = InferenceClient(model=f"{user_name_hugging_face}/{model_name_hugging_face}", token=token_model)
except Exception as e:
    print("Exception: ")
    print(e)

print("I am after InferenceClient")
token_bot = "6983089788:AAEjOhXKEvSfct9sfsAE5nEOMUnOiTFhR04"
LABEL_COLUMNS = ["nsfw", "hate_speech", "bullying"]


def get_full_name(message):
    first_name = message.from_user.first_name
    first_name = first_name[0].upper() + first_name[1:]
    last_name = message.from_user.last_name
    last_name = last_name[0].upper() + last_name[1:]

    return first_name + ' ' + last_name


def convert_model_output_score_to_prediction(results):
    lst_rets = []

    for i, result in enumerate(results):
        score = result.score

        if score >= 0.5:
            lst_rets.append(LABEL_COLUMNS[i].replace("_", " "))

    if len(lst_rets) == 0:
        ret = "This message was approved"
    elif 1 == len(lst_rets):
        ret = f"This message was {lst_rets[0]}"
    elif 2 == len(lst_rets):
        ret = f"This message was {lst_rets[0]} and {lst_rets[1]}"
    else:
        ret = f"This message was {lst_rets[0]}, {lst_rets[1]}, and {lst_rets[2]}"

    return ret



# Define a function to handle the messages that the bot receives
def text_handler(update: Update, context: CallbackContext):
    # Get the message from the update
    message = update.message

    results = client.text_classification(message.text)
    str_prediction = convert_model_output_score_to_prediction(results)
    if str_prediction != "This message was approved":
        full_name = get_full_name(message)
        str_prediction = full_name + ': ' + str_prediction.lower()
        message.delete()
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text=str_prediction)
        return


def photo_handler(update: Update, context: CallbackContext):
    message = update.message
    full_name = get_full_name(message)
    output_str = f"{full_name}: Pictures are not allowed"
    message.delete()
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=output_str)


def video_handler(update: Update, context: CallbackContext):
    message = update.message
    full_name = get_full_name(message)
    output_str = f"{full_name}: Videos are not allowed"
    message.delete()
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=output_str)


def audio_handler(update: Update, context: CallbackContext):
    message = update.message
    full_name = get_full_name(message)
    output_str = f"{full_name}: Audio is not allowed"
    message.delete()
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=output_str)


def voice_handler(update: Update, context: CallbackContext):
    message = update.message
    full_name = get_full_name(message)
    output_str = f"{full_name}: Voice is not allowed"
    message.delete()
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=output_str)


def main() -> None:
    updater = Updater(token_bot, use_context=True)
    updater.dispatcher.add_handler(MessageHandler(Filters.text, text_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.video, video_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.audio, audio_handler))
    updater.dispatcher.add_handler(MessageHandler(Filters.voice, voice_handler))
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    print("I am in main")
    main()
