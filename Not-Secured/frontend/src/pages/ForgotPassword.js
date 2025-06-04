import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import "../styles/forgotPassword.css";

function ForgotPassword() {
  const [step, setStep] = useState(1); // Step 1: Enter email, Step 2: Verify code
  const [email, setEmail] = useState("");
  const [recoveryCode, setRecoveryCode] = useState("");
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const navigate = useNavigate();

  const handleEmailSubmit = async (e) => {
    e.preventDefault();

    if (!email) {
      alert("Email is required!");
      return;
    }

    if (!/\S+@\S+\.\S+/.test(email)) {
      alert("Invalid email format.");
      return;
    }

    try {
      const response = await fetch(
        `http://localhost:5000/forgot_password?email=${encodeURIComponent(
          email
        )}`,
        {
          method: "POST",
        }
      );

      const data = await response.json();

      if (response.ok) {
        alert("A recovery code has been sent to your email.");
        setStep(2);
      } else {
        alert(`Error: ${data.message || "Something went wrong."}`);
      }
    } catch (error) {
      console.error("Error sending recovery email:", error);
      alert("An unexpected error occurred. Please try again.");
    }
  };

  const handleCodeSubmit = async (e) => {
    e.preventDefault();

    if (!recoveryCode) {
      alert("Recovery code is required!");
      return;
    }

    if (!newPassword || !confirmPassword) {
      alert("Both password fields are required!");
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
        `http://localhost:5000/change_password_with_verify_code?recovery_code=${encodeURIComponent(
          recoveryCode
        )}&email=${encodeURIComponent(email)}&new_password=${encodeURIComponent(
          newPassword
        )}`,
        {
          method: "POST",
        }
      );

      const data = await response.json();

      if (response.ok) {
        alert("Password has been changed successfully!");
        navigate("/login");
      } else {
        alert(`Error: ${data.message || "Something went wrong."}`);
      }
    } catch (error) {
      console.error("Error changing password:", error);
      alert("An unexpected error occurred. Please try again.");
    }
  };

  return (
    <>
      <main>
        <div className="login-box">
          {step === 1 && (
            <>
              <h2>Forgot Password - Comunication_LTD</h2>
              <form onSubmit={handleEmailSubmit}>
                <input
                  type="email"
                  placeholder="Email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                />
                <button type="submit">Send Recovery Code</button>
              </form>
            </>
          )}

          {step === 2 && (
            <>
              <h2>Verify Recovery Code</h2>
              <form onSubmit={handleCodeSubmit}>
                <input
                  type="text"
                  placeholder="Type here the code"
                  value={recoveryCode}
                  onChange={(e) => setRecoveryCode(e.target.value)}
                  required
                />
                <button type="submit">Send Recovery Code</button>
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
                <button type="submit">Change Password</button>
              </form>
            </>
          )}
        </div>
      </main>
    </>
  );
}

export default ForgotPassword;
