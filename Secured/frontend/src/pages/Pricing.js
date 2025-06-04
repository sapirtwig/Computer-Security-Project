import React from "react";
import "../styles/pricing.css"; // אם אתה רוצה להוסיף עיצוב חיצוני

function Pricing() {
  return (
    <div className="mainPricing">
      <div className="plans-container">
        <div className="plan">
          <h3>Basic</h3>
          <ul>
            <li>✅ 2 GB Data</li>
            <li>✅ 3G/4G Support</li>
            <li>✅ No Contract</li>
            <li>✅ Email Support</li>
          </ul>
          <div className="price">$9.99 / month</div>
        </div>

        <div className="plan">
          <h3>Standard</h3>
          <ul>
            <li>✅ 10 GB Data</li>
            <li>✅ 4G LTE</li>
            <li>✅ Unlimited Calls</li>
            <li>✅ Priority Email Support</li>
          </ul>
          <div className="price">$19.99 / month</div>
        </div>

        <div className="plan">
          <h3>Premium</h3>
          <ul>
            <li>✅ 50 GB Data</li>
            <li>✅ 5G Ready</li>
            <li>✅ Unlimited Calls & Texts</li>
            <li>✅ 24/7 Live Chat Support</li>
          </ul>
          <div className="price">$39.99 / month</div>
        </div>

        <div className="plan">
          <h3>Business</h3>
          <ul>
            <li>✅ Unlimited Data</li>
            <li>✅ 5G Ultra Wideband</li>
            <li>✅ International Roaming</li>
            <li>✅ Dedicated Account Manager</li>
          </ul>
          <div className="price">$79.99 / month</div>
        </div>
      </div>
    </div>
  );
}

export default Pricing;
