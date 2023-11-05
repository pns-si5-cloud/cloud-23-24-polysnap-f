import React, { useEffect, useState } from "react";
import io from "socket.io-client";
import axios from "axios";
import { withRouter } from "react-router-dom";
import { useParams } from "react-router-dom";
import Card from "@mui/material/Card";
import CardContent from "@mui/material/CardContent";
import Typography from "@mui/material/Typography";
import Avatar from "@mui/material/Avatar";

const receiverURL = process.env.REACT_APP_RECEIVER_URL;
const posterURL = process.env.REACT_APP_POSTER_URL;
const wsURL = process.env.REACT_APP_WS_URL;
const READ_DURATION = 60 + 8;

const MessageListWrapper = (props) => {
  const { userID } = useParams();
  const { conversationId } = props;

  return <MessageList userID={userID} conversationId={conversationId} />;
};

class MessageList extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      messages: [],
    };
    this.fetchData = this.fetchData.bind(this);
  }

  async fetchData() {
    const userID = this.props.userID;
    const { conversationId } = this.props;
    try {
      console.log("convo ID", conversationId);
      const response = await fetch(
        `${receiverURL}/server/conversation/${conversationId}/history`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      );

      const data = await response.json();
      console.log("Fetched data:", data);
      const d = new Date();
      const utc = d.getTime() + d.getTimezoneOffset() * 60000;
      const currentTime = new Date(utc + 3600000 * "+0");
      console.log(currentTime);

      console.log("CURRENT TIME:", currentTime);
      const filteredData = data.filter((message) => {
        if (!message.smoke) {
          return true;
        }
        const messageTime = new Date(message.timestamp);
        const timeDifferenceInSeconds = (currentTime - messageTime) / 1000;

        console.log("Message:", message.text);
        console.log("Current time:", currentTime);
        console.log("Message time:", messageTime);
        console.log("Time difference:", timeDifferenceInSeconds);
        if (message.read_by.includes(userID)) {
          return timeDifferenceInSeconds <= READ_DURATION;
        } else {
          return !message.read_by.includes(userID);
        }
      });

      this.setState({ messages: filteredData });
      console.log(filteredData);

      for (const message of filteredData) {
        this.markAsRead(message.conversation_id, message._id);
      }
    } catch (error) {
      console.error("Error fetching or parsing messages:", error);
    }
  }

  componentDidMount() {
    this.fetchData();

    this.socket = io(
      "wss://app-7b3a3c98-565a-4b75-9e80-683f4e59b229.cleverapps.io"
    );

    this.socket.on("connect", () => {
      console.log("Connected to socket server.");
      console.log("Joining conversation:", this.props.conversationId);
      this.socket.emit("joinConversations", {conversation_ids: [this.props.conversationId] });
    });

    this.socket.on("newMessage", (message) => {
      console.log("New message received:", message);
      const data = JSON.parse(message);
      console.log("New message received:", data);
      this.markAsRead(data.conversation_id, data._id);
      this.setState((prevState) => ({
        messages: [...prevState.messages, data],
      }));
    });

    this.socket.on("disconnect", () => {
      console.log("Disconnected from socket server.");
    });
  }

  componentWillUnmount() {
    this.socket.disconnect();
  }

  componentDidUpdate(prevProps) {
    const element = document.querySelector(".conversation-h");
    element.scrollTop = element.scrollHeight;
    if (prevProps.conversationId !== this.props.conversationId) {
      this.fetchData();
      console.log("Leaving conversation:", prevProps.conversationId);
      this.socket.emit("leaveConversations", {conversation_ids: [prevProps.conversationId] });
      console.log("Joining conversation:", this.props.conversationId);
      this.socket.emit("joinConversations", {conversation_ids: [this.props.conversationId] });
    }
  }
  markAsRead = async (conversationId, messageId) => {
    console.log("Marking message as read...");
    console.log(conversationId);
    console.log(messageId);
    try {
      await axios.put(
        `${posterURL}/conversations/${conversationId}/messages/${messageId}/read`,
        { user_id: this.props.userID }
      );
    } catch (error) {
      console.error("Error marking the message as read:", error);
      console.log(error.response.data);
      console.log(error.response.status);
      console.log(error.response.headers);
    }
  };

  render() {
    const isUserMessage = (sender) => {
      return sender === this.props.userID;
    };

    return (
      <div>
        <h1 className="conversation">
          Message History - {this.props.conversationId}
        </h1>
        <ul
          className="conversation-h"
          style={{
            listStyleType: "none",
            padding: 0,
            overflowY: "auto",
            maxHeight: "800px",
          }}
        >
          {this.state.messages.map((message, index) => {
            return (
              <li
                key={index}
                style={{
                  display: "flex",
                  justifyContent: isUserMessage(message.sender)
                    ? "flex-end"
                    : "flex-start",
                  margin: "10px 0",
                  alignItems: "center",
                }}
              >
                {!isUserMessage(message.sender) && (
                  <Typography
                    variant="body2"
                    style={{ marginRight: "10px", fontWeight: "bold" }}
                  >
                    {message.sender}
                  </Typography>
                )}
                <Card
                  style={{
                    maxWidth: "70%",
                    borderRadius: "15px",
                    backgroundColor: isUserMessage(message.sender)
                      ? "#007BFF"
                      : "#f1f1f1",
                  }}
                >
                  <CardContent
                    style={{
                      display: "flex",
                      flexDirection: "column",
                      alignItems: isUserMessage(message.sender)
                        ? "flex-end"
                        : "flex-start",
                      color: isUserMessage(message.sender) ? "white" : "black",
                    }}
                  >
                    <Typography
                      variant="body1"
                      style={{ wordBreak: "break-word" }}
                    >
                      {message.text}
                    </Typography>

                    {message.image && (
                      <img
                        src={message.image}
                        alt="message-img"
                        style={{
                          maxWidth: "100%",
                          borderRadius: "10px",
                          marginTop: "8px",
                        }}
                      />
                    )}

                    <Typography
                      variant="body2"
                      style={{
                        marginTop: "8px",
                        color: isUserMessage(message.sender)
                          ? "rgba(255, 255, 255, 0.6)"
                          : "gray",
                      }}
                    >
                      {message.timestamp.split("T")[0].slice(5, 10)} :{" "}
                      {message.timestamp.split("T")[1].slice(0, 5)}
                    </Typography>
                  </CardContent>
                </Card>
              </li>
            );
          })}
        </ul>
      </div>
    );
  }
}

export default MessageListWrapper;
