class GetSubscribeRecordIdsMixin:
    def get_subscribes_record_ids(self, subscribes_by_blog):
        subscribes_record_ids = []
        for subscribe_by_blog in subscribes_by_blog:
            subscribes_record_ids.extend(
                [
                    subscribe_record.get('id')
                    for subscribe_record in subscribe_by_blog.subscribes_record.all().values('id')
                ]
            )
        return subscribes_record_ids