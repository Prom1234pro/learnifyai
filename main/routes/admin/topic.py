from ...models.models import db, Topic, Summary

def create_topic(summaries, **kwargs):
    topic = Topic(**kwargs)
    print(topic.id)
    db.session.add(topic)
    db.session.commit()
    for summary in summaries:
        summ = Summary(text=summary['text'], keynote=summary['keynote'], topic_id=topic.id)
        db.session.add(summ)
    db.session.commit()
    return topic.id