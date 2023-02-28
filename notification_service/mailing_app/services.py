def _get_statistick(mailing):
    messages = mailing.message_set.all()
    statistics = {
        f'Mailing id {mailing.id}': {
            'Sent messages': messages.filter(status='Sent').count(),
            'Not sent messages': messages.filter(status='Not sent').count()
        }
    }
    return statistics
    

def get_full_mailing_statistics(mailings):
    """Получение статистики по рассылкам"""
    statistics_for_mailings = [_get_statistick(mailing) for mailing in mailings]
    
    content = {
        'Number of mailings': mailings.count(),
        'Statistics': statistics_for_mailings
    }
    return content


def get_specific_mailing_statistics(mailing):
    """Получение статистики по конкретной рассылке"""
    content = _get_statistick(mailing)
    return content
