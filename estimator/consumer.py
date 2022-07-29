from channels.generic.websocket import AsyncWebsocketConsumer
import json

class DashConsumer(AsyncWebsocketConsumer):
    
    async def connect(self):
        self.groupname='dashboard'
        await self.channel_layer.group_add(
            self.groupname,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self,close_code):

        await self.channel_layer.group_discard(
            self.groupname,
            self.channel_name
        )
        
    

    async def receive(self, text_data):
        datapoint = json.loads(text_data)
        t = datapoint['temperature']
        p = datapoint['power']

        await self.channel_layer.group_send(
            self.groupname,
            {
                'type':'deprocessing',
                'temperature': t,
                'power': p,
            }
        )

        print ('>>>>',text_data)

        # pass

    async def deprocessing(self,event): 
        
        await self.send(text_data=json.dumps({'temperature': event['temperature'], 'power': event['power'], 'carbon': event['power']*1.2} ))