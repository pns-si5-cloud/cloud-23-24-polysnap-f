import React, { useEffect, useState } from "react";
import axios from "axios";
const posterURL = process.env.REACT_APP_POSTER_URL;
const receiverURL = process.env.REACT_APP_RECEIVER_URL;

const ConversationsList = ({
  userID,
  setSelectedConversation,
  selectedConversation,
}) => {
  const [conversations, setConversations] = useState([]);
  const [conversationsDetails, setConversationsDetails] = useState([]);
  const [showForm, setShowForm] = useState(false);
  const [participantIDs, setParticipantIDs] = useState([]);
  const [users, setUsers] = useState([]);
  const [readDuration, setReadDuration] = useState(5);
  const [refreshConversations, setRefreshConversations] = useState(false);

  useEffect(() => {
    axios
      .get(`${posterURL}/users/${userID}`)
      .then((response) => {
        setConversations(response.data.conversations);
        console.log("convos ", response.data);
        return Promise.all(
          response.data.conversations.map((convoID) =>
            axios.get(`${receiverURL}/server/conversation/${convoID}`)
          )
        );
      })
      .then((responses) => {
        const details = responses.map((response) => response.data);
        setConversationsDetails(details);
      })
      .catch((error) => {
        console.error("Error fetching conversations:", error);
      });
    axios
      .get(`${posterURL}/users`)
      .then((response) => {
        console.log("users ", response.data);
        setUsers(response.data);
      })
      .catch((error) => {
        console.error("Error fetching users:", error);
      });
  }, [userID, refreshConversations]);

  const createConversation = () => {
    const participantsArray = participantIDs.map((id) => ({ user_id: id }));
    participantsArray.push({ user_id: userID });

    axios
      .post(`${posterURL}/conversations`, {
        name: "New Conversation",
        participants: participantsArray,
        read_duration: Number(readDuration),
      })
      .then((response) => {
        const newConversation = response.data;
        console.log("new convo ", newConversation);
        if (!newConversation || !newConversation.participants) {
          throw new Error(
            "New conversation data is incomplete or not structured correctly."
          );
        }

        setRefreshConversations(!refreshConversations);

        const updatedParticipants = newConversation.participants.map(
          (participant) => ({
            ...participant,
            user_id: String(participant.user_id),
          })
        );

        setConversationsDetails((prevConversationsDetails) => [
          ...prevConversationsDetails,
          { ...newConversation, participants: updatedParticipants },
        ]);

        setConversations((prevConversations) => [
          ...prevConversations,
          newConversation._id,
        ]);
        setShowForm(false);
        setParticipantIDs([]);
        setReadDuration(5);
      })
      .catch((error) => {
        console.error("Error creating conversation:", error);
      });
  };

  const handleSelectConversation = (conversationID) => {
    setSelectedConversation(conversationID);
  };

  return (
    <div>
      <h2>Conversations</h2>
      {showForm && (
        <>
          <div>
            {users.map((user) => (
              <div key={user.user_id}>
                <label>
                  <input
                    type="checkbox"
                    value={user.user_id}
                    checked={participantIDs.includes(user.user_id)}
                    onChange={(e) => {
                      if (e.target.checked) {
                        setParticipantIDs([...participantIDs, e.target.value]);
                      } else {
                        setParticipantIDs(
                          participantIDs.filter((id) => id !== e.target.value)
                        );
                      }
                    }}
                  />
                  {user.user_id}
                </label>
              </div>
            ))}
          </div>
          <div>
            <label>
              Read Duration (minutes):
              <input
                type="number"
                value={readDuration}
                onChange={(e) => setReadDuration(e.target.value)}
                min="1"
              />
            </label>
          </div>
          <button onClick={createConversation}>Create Conversation</button>
        </>
      )}
      <button
        style={{
          background: "lightblue",
          padding: "10px",
          borderRadius: "5px",
          margin: "10px 0",
        }}
        onClick={() => setShowForm(!showForm)}
      >
        {showForm ? "Cancel" : "New Conversation"}
      </button>
      <ul style={{ listStyleType: "none", padding: 0 }}>
        {conversationsDetails.length > 0
          ? conversationsDetails.map((conversation, index) => {
              const participantNames = conversation.participants
                .filter((participantID) => participantID !== userID)
                .join(", ");

              return (
                <li
                  key={conversation._id}
                  style={{
                    padding: "10px",
                    cursor: "pointer",
                    backgroundColor:
                      selectedConversation === conversation._id
                        ? "lightgrey"
                        : "white",
                    border: "1px solid #ccc",
                    borderRadius: "5px",
                    display: "flex",
                    alignItems: "center",
                    marginBottom: "5px",
                  }}
                  onClick={() => handleSelectConversation(conversation._id)}
                >
                  <div
                    style={{
                      marginRight: "10px",
                      width: "20px",
                      height: "20px",
                      backgroundColor: "lightgray",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                      borderRadius: "50%",
                    }}
                  >
                    🗨️
                  </div>
                  {participantNames}
                </li>
              );
            })
          : "Loading or no conversations available."}
      </ul>
    </div>
  );
};

export default ConversationsList;
