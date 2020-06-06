#!/usr/bin/env python3
import logging
import requests
from telegram.ext import Updater, CommandHandler

import config

logging.basicConfig(level=logging.INFO)

def start(update, context):
    message = "This Bot shows covid 19 Statistics of India"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message
    )


def get_covid_india_cases():
    response = requests.get("https://api.covid19india.org/data.json")
    answer = response.json()
    statewise_list = answer["statewise"]
    return statewise_list


def get_covid_india_cases_total():
    statewise = get_covid_india_cases()
    # see, let's iterate over this array
    for state in statewise:
        if state["state"] == "Total":
            return int(state["confirmed"])


def covid_19_update(update, context):
    count = get_covid_india_cases_total()
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"The total Number of cases in india {count}"
    )


def confirmed_list(update, context):
    states = get_covid_india_cases()
    message = "State wise cases are:\n\n"
    for state in states:
        message += f"<code>{state['confirmed']:7} : {state['state']}</code>\n"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        parse_mode='html'
    )


def states_list(update, context):
    states = get_covid_india_cases()
    
    for state in states:
        message = f"""<b>{state['state']}</b>

Confirmed: <code>{state['confirmed']}</code>
Active: <code>{state['active']}</code>
Deaths: <code>{state['deaths']}</code>
"""
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            parse_mode="html"
        )
    


def deaths_list(update, context):
    states = get_covid_india_cases()
    message = "statewise deaths are:\n \n"
    for state in states:
        message += f"{state['state']} : {state['deaths']}\n"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text= message
    )


def active_cases(update, context):
    states = get_covid_india_cases()
    message = "statewise active cases are:\n \n"
    for state in states:
        message += f"{state['state']} : {state['active']}\n"
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text = message
    )




updater = Updater(token=config.TOKEN, use_context=True)
dispatcher  = updater.dispatcher

all_details_handler = CommandHandler('all_stats', states_list)
dispatcher.add_handler(all_details_handler)

active_handler = CommandHandler('active', active_cases)
dispatcher.add_handler(active_handler)

deaths_handler = CommandHandler('deaths', deaths_list)
dispatcher.add_handler(deaths_handler)

state_handler=CommandHandler('states', confirmed_list)
dispatcher.add_handler(state_handler)

total_case_handler = CommandHandler('total_case', covid_19_update)
dispatcher.add_handler(total_case_handler)

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
