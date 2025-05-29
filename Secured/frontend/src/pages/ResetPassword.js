import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/resetPassword.css";

function ResetPassword() {
  const [email, setEmail] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!email || !newPassword || !confirmPassword) {
      alert("All fields are required!");
      return;
    }

    if (!/\S+@\S+\.\S+/.test(email)) {
      alert("Invalid email format.");
      return;
    }

    if (newPassword.length < 10) {
      alert("Password must be at least 10 characters long.");
      return;
    }

    if (newPassword !== confirmPassword) {
      alert("Passwords do not match.");
      return;
    }

    try {
      const response = await fetch(
        `http://localhost:5000/change_password?email=${encodeURIComponent(
          email
        )}&new_password=${encodeURIComponent(newPassword)}`,
        {
          method: "POST",
        }
      );

      let data;
      try {
        data = await response.json();
      } catch (error) {
        console.error("Failed to parse response JSON:", error);
        data = null;
      }

      // הצגת הודעת הצלחה בכל מקרה בו הסיסמה שונתה בהצלחה
      if (
        response.ok ||
        (data && data.message?.toLowerCase().includes("password changed"))
      ) {
        alert("Password changed successfully!");
        navigate("/login");
      } else if (data && data.message) {
        // הודעה רק אם יש תוכן שגיאה ספציפי
        alert(`Error: ${data.message}`);
      }
    } catch (error) {
      console.error("Error resetting password:", error);
      // הודעה כללית רק במקרה של שגיאת רשת או בעיה חמורה
      alert("An unexpected error occurred. Please try again.");
    }
  };

  return (
    <>
      <main>
        <div className="login-box">
          <h2>Reset Password - Comunication_LTD</h2>
          <form onSubmit={handleSubmit}>
            <input
              type="email"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Type new password"
              value={newPassword}
              onChange={(e) => setNewPassword(e.target.value)}
              required
            />
            <input
              type="password"
              placeholder="Type password again"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
            />
            <button type="submit">Reset Password</button>
          </form>
        </div>
      </main>
    </>
  );
}

export default ResetPassword;
