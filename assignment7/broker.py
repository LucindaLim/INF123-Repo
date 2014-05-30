from network import Listener, Handler, poll


handlers = {}  # map client handler to user name
names = {} # map name to handler
subs = {} # map tag to handlers

def broadcast(msg):
    for h in handlers.keys():
        h.do_send(msg)


class MyHandler(Handler):
    
    def on_open(self):
        handlers[self] = None
        
    def on_close(self):
        name = handlers[self]
        del handlers[self]
        del names[name]
        for tag in subs.itervalues():
            if self in tag:
                tag.remove(self)
        broadcast({'leave': name, 'users': handlers.values()})
        
    def on_msg(self, msg):
        def subscribe(self, tag):
            if tag in subs:
                if self not in subs[tag]:
                    subs[tag]+=[self]
            else:
                subs[tag]=[self]
        def unsubscribe(self, tag):
            if tag in subs:
                if self in subs[tag]:
                    subs[tag].remove(self)
        def limited_broadcast(hs,msg):
            for h in hs:
                h.do_send(msg)
        if 'join' in msg:
            name = msg['join']
            handlers[self] = name
            names[name]=self
            broadcast({'join': name, 'users': handlers.values()})
        elif 'speak' in msg:
            name, txt = msg['speak'], msg['txt']
            target_tags=[]
            private_msg=[]
            for word in txt.split(' '):
                if word[:1]=="+":
                    subscribe(self,word[1:])
                elif word[:1]=="-":
                    unsubscribe(self,word[1:])
                elif word[:1]=="#":
                    target_tags+=[word[1:]]
                elif word[:1]=="@":
                    private_msg+=[word[1:]]
            if len(target_tags)==0 and len(private_msg)==0:
                broadcast({'speak': name, 'txt': txt})
            else:
                hs=set()
                for tag in target_tags:
                    if tag in subs:
                        for sub in subs[tag]:
                            hs.add(sub)
                for person in private_msg:
                    if person in names:
                        hs.add(names[person])
                limited_broadcast(hs,{'speak': name, 'txt': txt})

Listener(8888, MyHandler)
while 1:
    poll(0.05)
