# WLED Revive for Home Assistant

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![HACS Custom](https://img.shields.io/badge/HACS-Custom_Repository-orange)
![IoT Class](https://img.shields.io/badge/IoT_Class-Local_Polling-success)

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
