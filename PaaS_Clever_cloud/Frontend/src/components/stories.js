import React, { useState, useEffect } from "react";
import axios from "axios";

const receiverURL = process.env.REACT_APP_RECEIVER_URL;
const posterURL = process.env.REACT_APP_POSTER_URL;

const Stories = ({ userID }) => {
  const [stories, setStories] = useState({});
  const [showModal, setShowModal] = useState(false);
  const [showAddStoryModal, setShowAddStoryModal] = useState(false);
  const [currentImage, setCurrentImage] = useState(null);
  const [selectedUsers, setSelectedUsers] = useState([]);
  const [allUsers, setAllUsers] = useState([]);
  const [file, setFile] = useState(null);
  const [currentStoryIndex, setCurrentStoryIndex] = useState(0);
  const [currentUserId, setCurrentUserId] = useState(null);
  const [storyDuration, setStoryDuration] = useState(24); // default to 24 hours

  useEffect(() => {
    fetch(`${receiverURL}/server/users/${userID}/stories/viewable`)
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        let groupedStories = {};

        const userStories = data.filter((story) => story.user_id === userID);
        if (userStories.length && userStories[0].image_url) {
          groupedStories[userID] = userStories;
        }

        data.forEach((story) => {
          if (!story.image_url) {
            console.warn("Skipping story without image_url:", story);
            return;
          }
          if (story.user_id === userID) return;
          if (!groupedStories[story.user_id]) {
            groupedStories[story.user_id] = [];
          }
          groupedStories[story.user_id].push(story);
        });

        console.log("Grouped Stories:", groupedStories);
        setStories(groupedStories);
      })
      .catch((error) => console.error("Error fetching stories:", error));

    axios.get(`${posterURL}/users`).then((res) => setAllUsers(res.data));
  }, []);

  const handleAddStory = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    console.log("Selected file:", file);
    let signed_url;
    try {
      const response = await axios.get(`${posterURL}/upload-url`, {
        params: { content_type: file.type },
      });
      console.log("Response from server:", response.data);
      signed_url = response.data.signed_url;

      const headers = {
        "Content-Type": file.type,
      };

      await axios.put(signed_url, file, { headers: headers });
    } catch (error) {
      console.error("Error during story upload:", error);
    }
    setFile(signed_url.split("?")[0]);
    console.log("actual url ? :", signed_url.split("?")[0]);

    setShowAddStoryModal(true);
  };

  const handlePostStory = async () => {
    const viewerList = [...new Set([...selectedUsers, userID])].map(
      (userId) => ({ user_id: userId })
    );

    await axios.post(`${posterURL}/stories`, {
      user_id: userID,
      image_url: file,
      viewers: viewerList,
      duration: storyDuration,
    });
    setShowAddStoryModal(false);

    fetch(`${receiverURL}/server/users/${userID}/stories/viewable`)
      .then((response) => response.json())
      .then((data) => {
        let groupedStories = {};

        const userStories = data.filter((story) => story.user_id === userID);
        if (userStories.length && userStories[0].image_url) {
          groupedStories[userID] = userStories;
        }

        data.forEach((story) => {
          if (!story.image_url) {
            console.warn("Skipping story without image_url:", story);
            return;
          }
          if (story.user_id === userID) return;
          if (!groupedStories[story.user_id]) {
            groupedStories[story.user_id] = [];
          }
          groupedStories[story.user_id].push(story);
        });

        console.log("Updated Grouped Stories:", groupedStories);
        setStories(groupedStories);
      })
      .catch((error) =>
        console.error("Error fetching updated stories:", error)
      );
  };

  const openStory = (userId, index) => {
    setCurrentUserId(userId);
    setCurrentStoryIndex(index);
    setShowModal(true);
  };

  return (
    <>
      <div
        style={{ display: "flex", overflowX: "scroll", alignItems: "center" }}
      >
        <div style={{ marginRight: "10px" }}>
          <label style={{ cursor: "pointer" }}>
            <input
              type="file"
              style={{ display: "none" }}
              onChange={handleAddStory}
            />
            <div
              style={{
                width: "50px",
                height: "50px",
                borderRadius: "50%",
                background: "lightgray",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              +
            </div>
          </label>
        </div>
        {Object.keys(stories).map((userId) => (
          <div
            key={userId}
            onClick={() => openStory(userId, 0)}
            style={{
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              marginRight: "10px",
              cursor: "pointer",
            }}
          >
            {stories[userId] &&
              stories[userId][0] &&
              stories[userId][0].image_url && (
                <img
                  src={stories[userId][0].image_url}
                  alt={`Story by ${userId}`}
                  style={{ width: "50px", height: "50px", borderRadius: "50%" }}
                />
              )}
            <span>{userId}</span>
          </div>
        ))}
      </div>

      {showModal && currentUserId && (
        <div
          style={{
            position: "fixed",
            top: "50%",
            left: "50%",
            transform: "translate(-50%, -50%)",
            padding: "20px",
            background: "#fff",
            boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
            borderRadius: "8px",
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            zIndex: 1000,
          }}
        >
          <img
            src={stories[currentUserId][currentStoryIndex].image_url}
            alt="Selected story"
            style={{
              width: "300px",
              height: "400px",
              objectFit: "cover",
              marginBottom: "10px",
            }}
          />

          {/* Navigation section */}
          <div
            style={{
              display: "flex",
              justifyContent: "space-between",
              width: "100%",
            }}
          >
            {/* Previous arrow */}
            {currentStoryIndex > 0 && (
              <button
                onClick={() => setCurrentStoryIndex((prev) => prev - 1)}
                style={{
                  background: "none",
                  border: "none",
                  cursor: "pointer",
                  fontSize: "24px",
                }}
              >
                ←
              </button>
            )}

            {/* Close button in the middle */}
            <button
              onClick={() => setShowModal(false)}
              style={{
                background: "none",
                border: "none",
                cursor: "pointer",
                fontSize: "24px",
              }}
            >
              Close
            </button>

            {/* Next arrow */}
            {currentStoryIndex < stories[currentUserId].length - 1 && (
              <button
                onClick={() => setCurrentStoryIndex((prev) => prev + 1)}
                style={{
                  background: "none",
                  border: "none",
                  cursor: "pointer",
                  fontSize: "24px",
                }}
              >
                →
              </button>
            )}
          </div>
        </div>
      )}

      {showAddStoryModal && (
        <div
          style={{
            position: "fixed",
            top: 0,
            left: 0,
            width: "100vw",
            height: "100vh",
            backgroundColor: "rgba(0, 0, 0, 0.5)",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            flexDirection: "column",
            zIndex: 1000,
          }}
        >
          <h2>Select viewers for your story</h2>

          {/* Select All Option */}
          <div>
            <label>
              <input
                type="checkbox"
                onChange={(e) => {
                  if (e.target.checked) {
                    const allUserIds = allUsers
                      .map((user) => user.user_id)
                      .filter((id) => id !== userID);
                    setSelectedUsers(allUserIds);
                  } else {
                    setSelectedUsers([]);
                  }
                }}
              />
              <span style={{ marginLeft: "10px" }}>Select All</span>
            </label>
          </div>

          <div
            style={{
              padding: "20px",
              border: "1px solid #e0e0e0",
              borderRadius: "8px",
              maxHeight: "300px",
              overflowY: "scroll",
              backgroundColor: "aliceblue",
            }}
          >
            {allUsers.map(
              (user) =>
                user.user_id !== userID && (
                  <div
                    key={user.user_id}
                    style={{
                      display: "flex",
                      alignItems: "center",
                      marginBottom: "10px",
                    }}
                  >
                    <input
                      type="checkbox"
                      value={user.user_id}
                      checked={selectedUsers.includes(user.user_id)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setSelectedUsers((prev) => [...prev, e.target.value]);
                        } else {
                          setSelectedUsers((prev) =>
                            prev.filter((id) => id !== e.target.value)
                          );
                        }
                      }}
                      style={{ marginRight: "10px" }}
                    />
                    <span>{user.user_id}</span>
                  </div>
                )
            )}
          </div>
          <div style={{ margin: "10px 0" }}>
            <label htmlFor="storyDuration" style={{ marginRight: "10px" }}>
              Duration in hours:
            </label>
            <input
              id="storyDuration"
              type="number"
              value={storyDuration}
              onChange={(e) => setStoryDuration(e.target.value)}
              style={{ marginRight: "10px" }}
            />
          </div>
          <button onClick={handlePostStory}>Post Story</button>
        </div>
      )}
    </>
  );
};

export default Stories;
