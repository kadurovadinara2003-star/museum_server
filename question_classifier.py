def classify_question(text: str) -> str:
    text_lower = text.lower()
    
    # AUTHOR – только добавим пару синонимов
    author_keywords = [
        'кто создал', 'автор', 'чьим трудом', 'кем создан', 'архитектор', 'скульптор',
        'кто спроектировал', 'кем выполнен', 'кто является автором', 'чьей работы',
        'кто сделал', 'кем сделан'   # новые
    ]
    if any(word in text_lower for word in author_keywords):
        return 'author'
    
    # HISTORY – добавим "когда был/была/было"
    history_keywords = [
        'история', 'когда появился', 'откуда взялся', 'происхождение', 'как возник',
        'в каком году', 'год постройки', 'когда открыли', 'когда построили',
        'когда установили', 'дата', 'в каком веке', 'сколько лет назад',
        'когда был', 'когда была', 'когда было'   # новые
    ]
    if any(word in text_lower for word in history_keywords):
        return 'history'
    
    # FACT – без изменений
    fact_keywords = [
        'интересн', 'удивительн', 'необычн', 'факт', 'любопытн',
        'забавный случай', 'уникальный', 'самый удивительный'
    ]
    if any(word in text_lower for word in fact_keywords):
        return 'fact'
    
    # FULL_INFO – без изменений
    full_indicators = [
        'подробно', 'всё', 'детально', 'расскажи всё', 'опиши подробно',
        'полностью', 'развернуто', 'обстоятельно'
    ]
    if any(word in text_lower for word in full_indicators):
        return 'full_info'
    
    # SHORT_INFO – оставляем как в лучшей версии (len<6, short_indicators с 'когда','где','сколько')
    words = text_lower.split()
    short_by_length = len(words) < 6
    short_indicators = ['где', 'когда', 'сколько', 'какой высоты', 'из чего', 'в каком стиле']
    has_short_indicator = any(word in text_lower for word in short_indicators)
    has_tell_verb = any(word in text_lower for word in ['расскажи', 'опиши', 'поведай'])
    
    if (short_by_length or has_short_indicator) and not has_tell_verb:
        return 'short_info'
    
    return 'full_info'