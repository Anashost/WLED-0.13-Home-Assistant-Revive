<!-- anashost_support_badges_start -->
[![Revolut.Me][revolut_me_shield]][revolut_me]
[![PayPal.Me][paypal_me_shield]][paypal_me]
[![ko_fi][ko_fi_shield]][ko_fi_me]
[![buymecoffee][buy_me_coffee_shield]][buy_me_coffee_me]
[![patreon][patreon_shield]][patreon_me]
<!-- anashost_support_badges_end -->
<!-- 
```diff
- text in red
+ text in green
! text in orange
# text in gray
@@ text in purple (and bold)@@
```
-->

# WLED Revive for Home Assistant

**WLED Revive** is a custom integration for Home Assistant designed to restore full local control for older WLED controllers (like v0.13) that have lost native support in recent Home Assistant updates. 

If your older WLED boards are constantly showing as "Unavailable" or failing to connect using the official integration, WLED Revive bypasses the new websocket requirements and uses stable local HTTP polling to keep your lights shining.

## ✨ Features
* **Full Local Control:** No cloud connection required.
* **Core Light Controls:** Toggle On/Off, Brightness, and RGB Color selection.
* **Dynamic Effects:** Automatically fetches the effect list directly from your WLED board.
* **Optimistic UI:** Instant UI feedback when changing colors or states.
* **Easy Configuration:** Fully setup through the Home Assistant UI (Config Flow).
* **Customizable Polling:** Adjust the polling interval directly from the integration options.

---

## 📦 Installation

You can install this integration via HACS (Recommended) or Manually.

### Method 1: HACS (Recommended)
Since this integration is not yet in the default HACS store, you will need to add it as a custom repository.

1. Open Home Assistant and navigate to **HACS**.
2. Click on **Integrations**.
3. Click the three dots (`...`) in the top right corner and select **Custom repositories**.
4. In the "Repository" field, paste the URL of this repository:
   `https://github.com/Anashost/WLED-0.13-Home-Assistant-Revive`
5. In the "Category" dropdown, select **Integration**.
6. Click **Add**.
7. Close the custom repositories window. You should now see **WLED Revive** in your HACS store.
8. Click on it and select **Download** in the bottom right corner.
9. **Restart Home Assistant** to load the new integration.

### Method 2: Manual Installation
1. Download the latest code from this repository as a `.zip` file, or clone it via Git.
2. Inside the downloaded files, locate the `custom_components/wled_revive` directory.
3. Copy the entire `wled_revive` folder into your Home Assistant's `config/custom_components/` directory.
   *(If the `custom_components` folder does not exist, create it).*
4. **Restart Home Assistant**.

---

## ⚙️ Configuration

Once installed and Home Assistant is restarted, you can add your WLED light:

1. Go to **Settings** -> **Devices & Services**.
2. Click the **+ Add Integration** button in the bottom right.
3. Search for **WLED Revive** and select it.
4. Fill in the required details:
   * **Name:** The name you want to give your light (e.g., Desk LED).
   * **IP Address:** The local IP address of your WLED controller.
   * **Polling Interval:** How often Home Assistant should check the light's status (default is 5 seconds).
5. Click **Submit**.

### 💡 Important Recommendation
To ensure your connection remains stable, it is highly recommended to set a **Static IP (DHCP Reservation)** for your WLED board inside your Wi-Fi router's settings. This prevents the IP address from changing when your router restarts.

If your WLED IP address ever changes, you can update it easily by going to Settings -> Devices & Services -> WLED Revive -> **Configure**.

---

## 🛠️ Troubleshooting

**"Failed to connect to the WLED controller"**
* Ensure your WLED board is powered on and connected to your Wi-Fi network.
* Verify the IP address is correct by typing it into your web browser. You should see the native WLED interface.
* If your WLED device is frequently dropping off the network, try assigning it a static IP address in your router.

## 🤝 Credits
Developed and maintained by [@Anashost](https://github.com/Anashost).

---

[paypal_me_shield]: https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white

[paypal_me]: https://paypal.me/anasboxsupport

[revolut_me_shield]:
https://img.shields.io/badge/revolut-FFFFFF?style=for-the-badge&logo=revolut&logoColor=black

[revolut_me]: https://revolut.me/anas4e

[ko_fi_shield]: https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white

[ko_fi_me]: https://ko-fi.com/anasbox

[buy_me_coffee_shield]: 
https://img.shields.io/badge/Buy%20Me%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black

[buy_me_coffee_me]: https://www.buymeacoffee.com/anasbox

[patreon_shield]: 
https://img.shields.io/badge/patreon-404040?style=for-the-badge&logo=patreon&logoColor=white

[patreon_me]:  https://patreon.com/AnasBox

