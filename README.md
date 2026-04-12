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

<div align="center">

  <img src="custom_components/wled_revive/brand/logo.png" alt="WLED Revive Logo" width="150" />

  # WLED Revive

  **Breathe life back into your older WLED hardware inside Home Assistant.**

</div>

🚨 **NOTICE: THE NEW NATIVE INTEGRATION IS HERE!**
> WLED Revive has been completely rebuilt as a native Home Assistant Custom Component (Config Flow). If you are looking for the old, manual YAML/Script workaround, it has been safely archived in [`OLD_WAY.md`](OLD_WAY.md).

---

## 📖 The Story: Why does this exist?

WLED is undeniably one of the greatest open-source lighting projects in the world. However, as the software grew more powerful and feature-rich, the firmware size naturally expanded. 

Eventually, the newer WLED updates (v0.14+) became **too large to fit on older ESP8266 boards** (like those with only 1MB or 2MB of memory). Those devices were permanently stuck on **v0.13.x or older**. 

Recently, the official Home Assistant WLED integration was updated to strictly require modern WebSockets for communication. Because older firmware couldn't handle this properly, **v0.13 and older controllers broke entirely in Home Assistant**, constantly dropping off the network or showing as "Unavailable."

**WLED Revive comes to the rescue.** By reverting to WLED's highly stable, local HTTP JSON API via intelligent polling, this integration completely bypasses the WebSocket requirement. 

*(Bonus: Because it uses the standard API, **WLED Revive works flawlessly with brand-new WLED controllers too!** If you are having WebSocket stability issues with a modern board, WLED Revive is a fantastic alternative.)*

---

## ✨ Features

* 🚀 **Full Local Control:** 100% cloud-free, hyper-local communication.
* ⚡ **Core Lighting Support:** Seamless toggling, brightness control, and RGB color selection.
* 🎨 **Dynamic Effect Fetching:** Automatically reads the list of effects directly from your specific WLED board.
* 🧠 **Optimistic UI:** Instant feedback in the Home Assistant dashboard when changing colors or states—no waiting for the next poll cycle.
* ⚙️ **Easy Configuration:** Set up everything directly through the Home Assistant UI. No YAML required.
* ⏱️ **Custom Polling:** Adjust the polling interval (down to the second) to balance responsiveness and network traffic.

---

## 📦 Installation

<details>
<summary><b>Method 1: HACS (Recommended)</b></summary>
<br>
Since this integration is brand new, you will need to add it as a custom repository in HACS:

1. Open Home Assistant and navigate to **HACS** > **Integrations**.
2. Click the three dots (`...`) in the top right corner and select **Custom repositories**.
3. In the "Repository" field, paste this URL:
   `https://github.com/Anashost/WLED-0.13-Home-Assistant-Revive`
4. In the "Category" dropdown, select **Integration**.
5. Click **Add**, then close the window.
6. Search for **WLED Revive** in the HACS store, click it, and select **Download**.
7. **Restart Home Assistant** to load the integration.
</details>

<details>
<summary><b>Method 2: Manual Installation</b></summary>
<br>

1. Download the latest code from this repository as a `.zip` file.
2. Inside the downloaded files, locate the `custom_components/wled_revive` folder.
3. Copy the entire `wled_revive` folder into your Home Assistant's `config/custom_components/` directory. *(Create the `custom_components` folder if it doesn't exist).*
4. **Restart Home Assistant**.
</details>

---

## 🛠️ Configuration

Once installed and Home Assistant is restarted, connecting your lights takes seconds:

1. Go to **Settings** -> **Devices & Services**.
2. Click the **+ Add Integration** button in the bottom right corner.
3. Search for **WLED Revive**.
4. Fill in the details:
   * **Name:** A friendly name (e.g., *Kitchen Cabinets*).
   * **IP Address:** The local IP address of your WLED controller.
   * **Polling Interval:** How often to check the light's status (Default: `5` seconds).

> 💡 **Pro-Tip:** To prevent connection issues later, log into your Wi-Fi router and set a **Static IP (DHCP Reservation)** for your WLED board. This ensures the IP address never changes!

---

## 🚑 Troubleshooting

<details>
<summary><b>"Failed to connect to the WLED controller"</b></summary>
<ul>
  <li>Ensure your WLED board is powered on and connected to your Wi-Fi.</li>
  <li>Type the IP address directly into your computer/phone's web browser. If the WLED interface doesn't load, Home Assistant can't see it either.</li>
  <li>If the IP address changed, simply go to Settings -> Devices & Services -> WLED Revive -> <b>Configure</b> to update it.</li>
</ul>
</details>

<details>
<summary><b>The light takes a few seconds to update when changed from outside HA (like the WLED App)</b></summary>
<p>This is normal! Because this integration uses local polling instead of WebSockets to maintain compatibility with older boards, Home Assistant only asks the board for its status every X seconds. You can lower the "Polling Interval" in the integration options if you want it to update faster.</p>
</details>

---

<div align="center">
  <i>Developed with ❤️ to keep perfectly good hardware out of landfills.</i><br>
  Maintained by <a href="https://github.com/Anashost">@Anashost</a>
</div>

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

