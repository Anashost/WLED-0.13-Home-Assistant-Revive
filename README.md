

<div align="center">

  <a href="https://github.com/Anashost/WLED-0.13-Home-Assistant-Revive">
    <img src="custom_components/wled_revive/brand/logo.png" alt="WLED Revive Logo" width="180" />
  </a>

  <br>

  # WLED Revive
  
  **Breathe life back into your older WLED hardware inside Home Assistant.**

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

  <p>
    <i>Bypassing modern WebSocket requirements to keep your perfectly good hardware out of landfills.</i>
  </p>

</div>

<br>

> 🚨 **NOTICE: THE NEW NATIVE INTEGRATION IS HERE!** <br>
> WLED Revive has been completely rebuilt as a native Home Assistant Custom Component (Config Flow). If you are looking for the old, manual YAML/Script workaround, it has been safely archived in [`OLD_WAY.md`](OLD_WAY.md).

<br>

## ✨ Next-Level Features

<table>
  <tr>
    <td align="center" width="33%">
      <h3>🚀 Full Local Control</h3>
      <p>100% cloud-free, hyper-local HTTP communication. No internet required.</p>
    </td>
    <td align="center" width="33%">
      <h3>🎨 Dynamic Effects</h3>
      <p>Automatically fetches and builds the exact effect list from your specific board.</p>
    </td>
    <td align="center" width="33%">
      <h3>🧠 Optimistic UI</h3>
      <p>Instant visual feedback in your Home Assistant dashboard. No waiting for polls.</p>
    </td>
  </tr>
</table>

<br>

## 📖 The Story: Why does this exist?

WLED is one of the greatest open-source lighting projects in the world. But as the software grew, the firmware became **too large to fit on older ESP8266 boards** (1MB/2MB memory). Those devices were permanently stuck on **v0.13.x**. 

Recently, the official Home Assistant WLED integration updated to strictly require modern WebSockets. Because older firmware couldn't handle this properly, **v0.13 and older controllers broke entirely in Home Assistant**.

**WLED Revive is the bridge.** By reverting to WLED's highly stable local HTTP API via intelligent polling, this integration completely bypasses the WebSocket requirement. 

*(Bonus: Because it uses the standard API, WLED Revive works flawlessly with **brand-new WLED controllers** too! If you have WebSocket instability on a modern board, WLED Revive is a fantastic alternative.)*

<br>

## 📦 Installation

### Method 1: HACS (Recommended)

1. Open Home Assistant and navigate to **HACS** > **Integrations**.
2. Click the `...` menu in the top right and select **Custom repositories**.
3. Paste this URL:
```
https://github.com/Anashost/WLED-0.13-Home-Assistant-Revive
```
5. Select **Integration** as the category and click **Add**.
6. Search for **WLED Revive** in the HACS store, download it, and **Restart Home Assistant**.

### Method 2: Manual Installation
<details>
<summary><i>Click here for manual install instructions</i></summary>
<br>
1. Download this repository as a `.zip` file.<br>
2. Locate the `custom_components/wled_revive` folder.<br>
3. Copy the entire folder into your Home Assistant's `config/custom_components/` directory.<br>
4. <b>Restart Home Assistant</b>.
</details>

<br>

## ⚙️ Configuration

Set up takes seconds directly from the UI:

1. Go to **Settings** -> **Devices & Services**.
2. Click **+ Add Integration** and search for **WLED Revive**.
3. Enter your details:
   * **Name:** e.g., *Kitchen Cabinets*
   * **IP Address:** *192.168.1.100*
   * **Polling Interval:** *(Default: 5 seconds)*

> 💡 **Pro-Tip:** Log into your Wi-Fi router and set a **Static IP (DHCP Reservation)** for your WLED board so the IP address never changes!

<br>

<div align="center">
  <img src="https://capsule-render.vercel.app/api?type=waving&color=0055ff&height=100&section=footer" width="100%" />
  <br>
  <i>Developed and maintained by <a href="https://github.com/Anashost">@Anashost</a></i>
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

