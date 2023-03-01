from django.db.models import Count, Q
from .models import Mailing

def _get_statistick(mailing):
    statistics = {
        f'Mailing id {mailing.id}': {
            'Sent': mailing.sent,
            'Not sent': mailing.not_sent
        }
    }
    return statistics
    

def get_mailing_statistics(pk=None):
    """Получение статистики по рассылкам"""   
    sent = Count('message', filter=Q(message__status=True))
    not_sent = Count('message', filter=Q(message__status=False))
    pk_filter = {'id': pk} if pk else {}

    mailings = Mailing.objects.\
        filter(**pk_filter).\
        annotate(not_sent=not_sent).\
        annotate(sent=sent)

    statistics_for_mailings = [_get_statistick(mailing) for mailing in mailings]    
    content = {
        'Number of mailings': mailings.count(),
        'Statistics': statistics_for_mailings
    }
    return content
