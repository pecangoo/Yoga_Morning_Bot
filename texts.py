
def left_classes(id:int, dict_users:dict):
    texts = str()
    # Если занятия есть, показываем количество занятий
    # Если занятий нет, предлагаем подписаться.
    if dict_users[str(id)][1] == 0:
        texts = ("У вас нет доступных занятий. Чтобы приобрести подписку, нажмите /follow, "
                "или выберете соответствуюший пункт в меню")
    else:
        texts = f"Доступных занятий осталось: {dict_users[str(id)][1]}\n"
    return texts

text_zero_classes = "Чтобы получить занятие, вам необходимо оформить подписку\n"

#follow_text = "Дохуя умный текст, предложение подписки и выбор количества занятий"

def follow_text(sale:bool):
    text = ""
    text += "Вы можете приобрести подписку на 5, 10 или 30 дней\n"
    text += "Приступить к занятию вы можете в любое время выбрав пункт в меню \" Приступить к занятию \" \n"
    if sale:
        text += ("Стоимость пакетов занятий.\n"
                "5 занятий - 1̶7̶5̶0̶р̶ 1400р\n"
                "10 занятий - 3̶0̶0̶0̶р̶ 2400р\n"
                "30 занятий - 6̶0̶0̶0̶р̶ 4800р\n")
    else:
        text += ("Стоимость пакетов занятий.\n"
                 "5 занятий - 1750р\n"
                 "10 занятий - 3000р\n"
                 "30 занятий - 6000р\n")
    return text



agreement_text = ("    Продолжая оплату, вы соглашаетесь на покупку выбранного курса. "
                "Занятия будут присылаться согласно выбранному расписанию и времени. "
                "Выбор времени занятия будет доступен после оплаты.\n"

                "Данный Бот подключен к платежной системе ЮKassa. После перехода по ссылке 'Перейти на страницу оплаты'"
                " вы перейдете на сайт оплаты системы Юкасса. Все данные отправляются в зашифрованном виде и "
                "обрабатываются непосредственно платежной системой. Больше о безопасности платежей можно почитать тут"
                "→ (https://yookassa.ru/docs/support/security)\n"
                "Если вам необходимо будет отменить оплату, обратитесь к администратору в резделе /contacts "
                "или по кнопке в соответствующем пункте меню.")


greetting_text = ("Приветствую тебя на утренних занятиях йогой - Пробуждение🙏🏼\n\n"
    "☀️Ранние подъемы и утренняя зарядка - это привычка успешных и здоровых людей.\n"
    "Она формирует дисциплину, вносит порядок в жизнь, дает свободное время, делает тело здоровым, молодым и активным.\n\n"
    "☝️Регулярно занимаясь утренней йогой, ты раскроешь свое тело, подаришь ему здоровье, "
    "красоту и хорошее самочувствие на весь день. А  утренние подъемы станут для тебя легче "
    "и будут приносить удовольствие.\n\n"
    "⏳Удели себе внимание всего лишь 30 минут утром и ты увидишь, каким станет твой день и как это изменит твою жизнь.\n\n"
    "🤸Занятия доступны для каждого и не требуют специальной подготовки.\n"
    "Во время занятия мы:\n"
    "🔺Делаем дыхательные практики\n"
    "🔺Работаем со спиной, шеей и суставами\n"
    "🔺Укрепляем мышцы\n"
    "🔺Раскрываем тазобедренные суставы и придаем гибкость телу\n"
    "🔺Укрепляем иммунитет\n"
    "🔺Стабилизируем нервную систему\n")


text_after_try_class = ("Регулярные занятия йогой заметно улучшают самочувствие и делают тело здоровым и сильным. "
             "Главное не останавливайся в своем намерении.\n"
             "Тем более, в течении трех часов на приобретение занятий действует скидка 20%.\n")

text_two_weeks = ("Привет, твое тело соскучилась по тренировке?\n"
                  "Почувствовало скованность и появилась утомляемость?\n"
                    "Тогда не затягивай, возобнови занятия, сделай это прямо сейчас.\n")

text_no_two_weeks = ("Твое тело не станет красивым, здоровым и молодым, если ты не сделаешь этот шаг. "
                    "Только регулярные нагрузки и движения сделают это. Выбери жизнь активного и здорового человека,🤸✨ х"
                    "орошего самочувствия и настроения.\n\n"
                    "⚡Присоединяйся к занятиям прямо сейчас и получи бонусом медитацию для расслабления.🙏🏼\n")