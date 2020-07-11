Challenge Week 2
1. What is the purpose await / async, and in what situations would we want to use that?

Async and await keywords are used in Javascript for asynchronous operations. These operations are put into an event queue, which runs after main thread is finished processing. The reason / advantage for this is that the asynchronous operation does not block other operations in main thread and is handled once the async operation is finished running. 

2. The context module acts like a global service which provides access to actions and services to all React components. 

3. Too late in the night to make Loom video, but I will try to explain the paths below. Explain path when user 1 send message on channel 3 and: 
a. User 2 is on channel 3
Client-side
User 2 see messages as rendered by the Chat component (displays messages) and Message Component (creates message object to be sent). User 2 types into input box as rendered by InputMessage component where it updates the state of the written text. When pressing enter, the chat component prepares the message by calling chatService.prepareMessage() and then sends message using socketService.send() with event-name "send-message". 

Server-side
Message is received by socket-listener with "send-message" event. As a channel message, it is stored into the database using message_service.store_channel_message(). From here, the message is sent back to the channel on the client-side using "message-received" event-name. 

Client-side
Upon receiving the message, the message is handled by chatService.onMessageReceived() where the message is added to the message$ subject stream with next(). Back in the Chat component, the message$ subject stream is already subscribed (services.chatService.getMessages$), where message content along with time and sender information to show up. messageReceived() from actions.channel is also called with message argument, in which the channel message is dispatched with receivedChannelMessage action to update the state of channelId and message. 

b. User 3 is on channel #4.
Client-side
The above will happen when user 1 sends the message, but since the user is not currently on channel 3, he/she is on channel #4 and will have to fetch the messages when selecting the channel. When selecting channel 4 in the sidebar component, selectChannel() from actions.sidebar is called with channel 4's id passed as an argument. This does several things: gets channels available, gets the id by using supplied argument and gets existing messages for selected channel. If no existing messages are available, then a fetch call is made to the server to grab the 25 most recent messages. 

Server-side 
Channel messages are fetched using a HTTP get request which is pointed to /channel-messages/ endpoint. When request is received with channel-id, a list of 25 messages for request channel is sent as a response back to client.

Client-side
The client receives the list of channel message objects. This does not need to be parsed and is packaged as part of payload to update the channelId and the message state with list of channel messages. When message state is updated, chat component re-renders and will loop through said messages for display. 

4. User Primer 
See code changes in client and server-side

We use a dictionary or JSON for searching purposes since it is easier to search using a key. For searching to occur on a list, you'll need to iterate through items (sorting algo or through entire list) to find desired item. 



