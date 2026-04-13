<div align="center">

  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:FF00FF,100:00FFFF&height=120&section=header" width="100%" />

  <a href="https://github.com/Anashost/WLED-0.13-Home-Assistant-Revive">
    <img src="custom_components/wled_revive/brand/logo.png" alt="WLED Revive Logo" width="180" />
  </a>

  <br><br>

  <a href="https://github.com/Anashost/WLED-0.13-Home-Assistant-Revive">
    <img src="https://readme-typing-svg.herokuapp.com?font=Orbitron&weight=700&size=26&pause=1000&color=00FFFF&center=true&vCenter=true&width=800&lines=REACTIVATE+LEGACY+HARDWARE;BYPASS+WEBSOCKET+REQUIREMENTS;LOCAL+HTTP+CONTROL" alt="Typing SVG" />
  </a>

  <p>
    <i>Restores Home Assistant compatibility for older WLED devices (v0.13 and below) stuck on legacy ESP8266 hardware.</i>
  </p>

  <a href="https://revolut.me/anas4e">
    <img src="https://img.shields.io/badge/revolut-FFFFFF?style=for-the-badge&logo=revolut&logoColor=black" alt="Revolut" />
  </a>
  <a href="https://paypal.me/anasboxsupport">
    <img src="https://img.shields.io/badge/PayPal-00457C?style=for-the-badge&logo=paypal&logoColor=white" alt="PayPal" />
  </a>
  <a href="https://ko-fi.com/anasbox">
    <img src="https://img.shields.io/badge/Ko--fi-F16061?style=for-the-badge&logo=ko-fi&logoColor=white" alt="Ko-Fi" />
  </a>
  <a href="https://www.buymeacoffee.com/anasbox">
    <img src="https://img.shields.io/badge/Buy%20Me%20Coffee-ffdd00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me A Coffee" />
  </a>
  <a href="https://patreon.com/AnasBox">
    <img src="https://img.shields.io/badge/patreon-404040?style=for-the-badge&logo=patreon&logoColor=white" alt="Patreon" />
  </a>
  <br><br>

> 🚨 **NOTICE: NATIVE INTEGRATION ONLINE** <br>
> WLED Revive is now a **Native Home Assistant Custom Component (Config Flow)**. No manual YAML required. The old manual scripts are archived in [OLD_WAY.md](OLD_WAY.md).

</div>

<br>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:FF00FF,100:00FFFF&height=4" width="100%" />

## ⚡ FEATURES

<table>
  <tr>
    <td align="center" width="33%">
      <h3>🌐 HTTP Polling</h3>
      <p>Bypasses WebSockets. Uses standard HTTP API communication.</p>
    </td>
    <td align="center" width="33%">
      <h3>🎨 Auto-Sync</h3>
      <p>Fetches the exact effect list and color palettes directly from your board.</p>
    </td>
    <td align="center" width="33%">
      <h3>🧠 Optimistic UI</h3>
      <p>Updates the Home Assistant dashboard instantly, avoiding polling delay lag.</p>
    </td>
  </tr>
</table>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:00FFFF,100:FF00FF&height=4" width="100%" />

## 📖 What is this, exactly?

Modern updates to the official Home Assistant WLED integration mandate WebSocket support. ESP8266 boards with limited memory (1MB/2MB) cannot run newer WLED firmware and are permanently stuck on **v0.13.x**. Because v0.13 handles WebSockets poorly, these controllers stopped working in Home Assistant.

**WLED Revive** fixes this by reverting to WLED's stable local HTTP API. 

*(Note: This integration also functions as a fallback for newer WLED controllers experiencing WebSocket instability.)*

<br>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:FF00FF,100:00FFFF&height=4" width="100%" />

## 📦 INSTALLATION

### 🔵 METHOD 1: HACS (Recommended)

1. Open Home Assistant and navigate to **HACS** > **Integrations**.
2. Click the '...' menu in the top right and select **Custom repositories**.
3. Add this repository URL:
   > https://github.com/Anashost/WLED-0.13-Home-Assistant-Revive
4. Set the category to **Integration** and click **Add**.
5. Search for **WLED Revive**, download it, and **Restart Home Assistant**.

### 🟣 METHOD 2: MANUAL
<details>
<summary><i>Click to expand manual installation steps</i></summary>
<br>
1. Download this repository as a .zip file.<br>
2. Extract and locate the <code>custom_components/wled_revive</code> directory.<br>
3. Move the entire directory into your Home Assistant's <code>config/custom_components/</code> folder.<br>
4. <b>Restart Home Assistant</b>.
</details>

<br>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:00FFFF,100:FF00FF&height=4" width="100%" />

## ⚙️ CONFIGURATION

1. Go to **Settings** -> **Devices & Services**.
2. Click **+ Add Integration** and search for **WLED Revive**.
3. Enter your details:
   * **Name:** *Your device name*
   * **IP Address:** *192.168.1.100*
   * **Polling Interval:** *(Default: 5 seconds)*

> 💡 **Recommendation:** Set a **Static IP (DHCP Reservation)** for your WLED board in your router settings to prevent connection drops.

<br>

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:FF00FF,100:00FFFF&height=4" width="100%" />

## 🛠️ TROUBLESHOOTING

* **Device Offline:** Ensure your WLED board has power and is on the same network as Home Assistant.
* **Connection Lost:** Verify the IP address hasn't changed. Assign a Static IP.
* **Compatibility:** Requires Home Assistant version 2023.x or newer.

<br>

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0:00FFFF,100:FF00FF&height=100&section=footer" width="100%" />
  <br>
  <i>Developed by <a href="https://github.com/Anashost">@Anashost</a></i>
</div>
