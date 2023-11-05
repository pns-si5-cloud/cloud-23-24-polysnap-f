import React, { useState, useRef } from "react";
import axios from "axios";
import { useParams } from "react-router-dom";
import IconButton from "@mui/material/IconButton";
import SendIcon from "@mui/icons-material/Send";
import CancelIcon from "@mui/icons-material/Cancel";
import PhotoCameraIcon from "@mui/icons-material/PhotoCamera";
import InputAdornment from "@mui/material/InputAdornment";
import TextField from "@mui/material/TextField";
import InsertPhotoIcon from "@mui/icons-material/InsertPhoto";
import Checkbox from "@mui/material/Checkbox";
import FormControlLabel from "@mui/material/FormControlLabel";

const posterURL = process.env.REACT_APP_POSTER_URL;

const MessageInput = (props) => {
  const { userID } = useParams();
  const [smoke, setSmoke] = useState(true);

  const [formData, setFormData] = useState({
    user_id: "",
    text: "",
    url: "",
  });
  formData.user_id = userID;

  const [file, setFile] = useState(null);
  const fileInputRef = useRef(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevState) => ({ ...prevState, [name]: value }));
  };

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    e.target.blur();
  };

  const handleUploadClick = () => {
    fileInputRef.current.click();
  };

  const handleRemoveFile = () => {
    setFile(null);
  };

  const handleSend = async () => {
    if (!formData.text && !file) {
      console.log("Nothing to send.");
      return;
    }

    try {
      let isFileUploaded = false;
      let isFormSubmitted = false;
      formData.smoke = smoke;

      if (file) {
        try {
          const response = await axios.get(`${posterURL}/upload-url`, {
            params: { content_type: file.type },
          });
          console.log("Response from server:", response.data);
          const { signed_url } = response.data;
          const headers = {
            "Content-Type": file.type,
          };

          await axios.put(signed_url, file, { headers: headers });
          console.log("File uploaded successfully.");
          formData.url = signed_url.split("?")[0];
          console.log("formData:", formData);
          isFileUploaded = true;
          setFile(null);
        } catch (error) {
          console.log("Error while uploading the file: ", error);
          if (error.response) {
            console.log("Server Response:", error.response.data);
          }
          return;
        }
      }
      if (formData.user_id || formData.text) {
        try {
          const messageData = {
            ...formData,
            smoke: smoke,
          };
          const headers = {
            "Content-Type": "application/json",
          };
          await axios.post(
            `${posterURL}/conversations/${props.conversationId}/messages`,
            messageData,
            { headers }
          );
        } catch (error) {
          console.log("Error while submitting the form: ", error);
          return;
        }

        isFormSubmitted = true;
      }

      if (isFileUploaded && isFormSubmitted) {
        console.log("Both file and form submitted successfully.");
        setFormData((prevState) => ({ ...prevState, text: "", url: "" }));
      } else if (isFileUploaded) {
        console.log("File uploaded successfully.");
        setFormData((prevState) => ({ ...prevState, text: "", url: "" }));
      } else if (isFormSubmitted) {
        console.log("Form submitted successfully.");
      } else {
        console.log("Nothing to send.");
      }

      if (fileInputRef.current) {
        fileInputRef.current.value = null;
      }
    } catch (error) {
      console.log("Error in handleSend function:", error);
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (document.activeElement !== fileInputRef.current) {
      handleSend();
      setFormData((prevState) => ({ ...prevState, text: "", url: "" }));
      fileInputRef.current.value = null;
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      className="inputs"
      style={{ display: "flex", alignItems: "center", width: "100%" }}
    >
      <FormControlLabel
        control={
          <Checkbox
            checked={!smoke}
            onChange={(e) => setSmoke(!e.target.checked)}
            name="smoke"
          />
        }
        label="Save"
      />
      <TextField
        variant="outlined"
        name="text"
        value={formData.text}
        onChange={handleChange}
        placeholder="Message"
        style={{ flex: 1, marginRight: "8px" }}
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <IconButton color="primary" onClick={handleUploadClick}>
                <InsertPhotoIcon />
              </IconButton>
            </InputAdornment>
          ),
        }}
      />
      {file && (
        <div style={{ position: "relative", marginRight: "8px" }}>
          <img
            src={URL.createObjectURL(file)}
            alt="Selected"
            style={{
              width: "40px",
              height: "40px",
              objectFit: "cover",
              borderRadius: "5px",
            }}
          />
          <IconButton
            color="secondary"
            size="small"
            style={{ position: "absolute", right: "-5px", top: "-5px" }}
            onClick={handleRemoveFile}
          >
            <CancelIcon />
          </IconButton>
        </div>
      )}
      <div style={{ display: "none" }}>
        <input type="file" ref={fileInputRef} onChange={handleFileChange} />
      </div>
      <IconButton color="primary" type="submit">
        <SendIcon />
      </IconButton>
    </form>
  );
};

export default MessageInput;
