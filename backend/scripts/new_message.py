from apps.chat.models import *
from faker import Faker
import os
import random
from random import choice, randrange

f = Faker()


class Mock:
    def __init__(self):
        pass

    def fk_sen(self):
        return f.sentence(randrange(8, 10))

    def gen_msg(self, conv_id, sender, msg_content):
        conv = Conversation.objects.get(pk=conv_id)
        receiver = conv.get_other_member(sender)
        msg = Message.objects.create(
            conversation=conv, sender=sender, receiver=receiver, content=msg_content)

    def gen_conv(self, conv_id, n=5):
        conv = Conversation.objects.get(pk=conv_id)
        for i in range(0, n):
            members = list(conv.members.all())
            msg_content = self.fk_sen()
            self.gen_msg(conv_id, sender=choice(members), msg_content=msg_content)
