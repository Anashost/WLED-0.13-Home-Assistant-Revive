[![Community Forum][community_forum_shield]][community_forum]<!-- anashost_support_badges_start -->
[![Revolut.Me][revolut_me_shield]][revolut_me]
[![PayPal.Me][paypal_me_shield]][paypal_me]
[![ko_fi][ko_fi_shield]][ko_fi_me]
[![buymecoffee][buy_me_coffee_shield]][buy_me_coffee_me]
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

# WLED 0.13.x LED Controller Home Assistant Revive
>Got an old WLED controller stuck on version v0.13.x, or any version below v0.14.0? Don’t worry.. your trusty little device isn’t destined for the junk drawer just yet! Even though those 1MB flash controllers can’t handle the latest WLED updates, there’s a fun and creative way to make those unsupported controller work seamlessly with the latest Home Assistant versions. In my case i have "7" unsupported controllers stuck at v0.13.1 and v0.13.3, so making them work again in Home Assistant was a win.

### Updates:
- `24 Dec 2024`: now working as two way communication using HTTP Polling. See **step 7**.
- `14 Jan 2025`: effect list fixed: removed newer effects that do not exist in wled v0.13.1.

### Working features:
- on
- off
- change color
- change brightness
- change effect

Tested on WS2812b LED

<div style="text-align:center">
    <img src="https://github.com/user-attachments/assets/811b13db-88dd-43de-95dd-0ddf735c4bd6" style="display:inline-block; width:35%; max-width:150px; margin:20px auto;">
    <img src="https://github.com/user-attachments/assets/bb4305e1-7c9f-41f4-95dc-54f79120ef26" style="display:inline-block; width:35%; max-width:150px; margin:20px auto;">
</div>


<hr>

Lets say we want our new light name to be `light.wled_desk_led` start by doing the following:

## 1 - Preparations

- Make sure to remove the unsupported led's from Wled integration.

- If not already, start by creating those files in Home Assistant root directory
`rest_command.yaml`,  `lights.yaml`, `input_select.yaml`

- include them in your `configuration.yaml`:

```
input_select: !include input_select.yaml
rest_command: !include rest_command.yaml
light: !include lights.yaml
```

- To make thing easy, use a text editor (Find & Replace All) tool to replace the word `desk` and `Desk` with the name you want. make sure to replace it everywhere and to double check, before coming yalling at me ;-)

- You have to do all the steps below for EVERY controller you have.

## 2 - Create a rest command to communicate with WLED controller:

* paste the rest command to your `rest_command.yaml`
* replace ip with your conroller ip

<details>
  <summary>rest command</summary>
  
```
  wled_desk_led:
    url: "http://10.0.0.107/win&T={{ on }}&A={{ brightness }}&R={{ red }}&G={{ green }}&B={{ blue }}{% if effect is defined %}&FX={{ effect }}{% endif %}"
```
</details>
  
## 3 - Create a light template:

* paste this to your `lights.yaml`

<details>
  <summary>light template</summary>
  
```
  - platform: template
    lights:
      wled_desk_led:
        friendly_name: "WLED Desk LED"
        value_template: "{{ states('input_boolean.wled_desk_led_state') == 'on' }}"
        level_template: "{{ states('input_number.wled_desk_led_brightness') | int }}"
        effect_list_template: "{{ state_attr('input_select.wled_desk_led_effect', 'options') }}"
        effect_template: "{{ states('input_select.wled_desk_led_effect') }}"
        rgb_template: >
          ({{ states('input_number.wled_desk_led_red') | int }},
           {{ states('input_number.wled_desk_led_green') | int }},
           {{ states('input_number.wled_desk_led_blue') | int }})
        turn_on:
          service: script.wled_desk_led_active
          data:
            brightness: "{{ states('input_number.wled_desk_led_brightness') | int }}"
            red: "{{ states('input_number.wled_desk_led_red') | int }}"
            green: "{{ states('input_number.wled_desk_led_green') | int }}"
            blue: "{{ states('input_number.wled_desk_led_blue') | int }}"
        turn_off:
          service: script.wled_desk_led_off
          data:
            brightness: "{{ states('input_number.wled_desk_led_brightness') | int }}"
            red: "{{ states('input_number.wled_desk_led_red') | int }}"
            green: "{{ states('input_number.wled_desk_led_green') | int }}"
            blue: "{{ states('input_number.wled_desk_led_blue') | int }}"
        set_level:
          service: script.wled_desk_led_active
          data:
            brightness: "{{ brightness }}"
        set_rgb:
          service: script.wled_desk_led_active
          data:
            brightness: "{{ states('input_number.wled_desk_led_brightness') | int }}"
            red: "{{ r }}"
            green: "{{ g }}"
            blue: "{{ b }}"
        set_effect:
          service: script.wled_desk_led_effect
          data:
            effect: "{{ effect }}"
```
</details>

## 4 - Create those 3 scripts:
those scripts are used to pass rest commands to your controller. Paste them to your `scripts.yaml`.

<details>
  <summary>script 1 - On/activities</summary>
  
```
wled_desk_led_active:
  alias: wled desk led active
  sequence:
  - action: input_boolean.turn_on
    target:
      entity_id:
      - input_boolean.wled_desk_led_state
    data: {}
    enabled: true
  - data:
      entity_id: input_number.wled_desk_led_brightness
      value: '{{ brightness | default(states(''input_number.wled_desk_led_brightness'')
        | int) }}'
    action: input_number.set_value
    enabled: true
  - data:
      entity_id: input_number.wled_desk_led_red
      value: '{{ red | default(states(''input_number.wled_desk_led_red'') | int) }}'
    action: input_number.set_value
    enabled: true
  - data:
      entity_id: input_number.wled_desk_led_green
      value: '{{ green | default(states(''input_number.wled_desk_led_green'') | int)
        }}'
    action: input_number.set_value
    enabled: true
  - data:
      entity_id: input_number.wled_desk_led_blue
      value: '{{ blue | default(states(''input_number.wled_desk_led_blue'') | int)
        }}'
    action: input_number.set_value
    enabled: true
  - data:
      'on': '{{ ''1'' if brightness | int > 0 else ''0'' }}'
      brightness: '{{ brightness | default(states(''input_number.wled_desk_led_brightness'')
        | int) }}'
      red: '{{ red | default(states(''input_number.wled_desk_led_red'') | int) }}'
      green: '{{ green | default(states(''input_number.wled_desk_led_green'') | int)
        }}'
      blue: '{{ blue | default(states(''input_number.wled_desk_led_blue'') | int)
        }}'
    action: rest_command.wled_desk_led
    enabled: true
  description: ''
```

</details>

<details>
  <summary>script 2 - Off</summary>
  
```
wled_desk_led_off:
  alias: Wled desk led off
  sequence:
  - action: rest_command.wled_desk_led
    data:
      'on': 0
      brightness: '{{ brightness | default(states(''input_number.wled_desk_led_brightness'')
        | int) }}'
      red: '{{ red | default(states(''input_number.wled_desk_led_red'') | int) }}'
      green: '{{ green | default(states(''input_number.wled_desk_led_green'') | int)
        }}'
      blue: '{{ blue | default(states(''input_number.wled_desk_led_blue'') | int)
        }}'
  - action: input_boolean.turn_off
    metadata: {}
    data: {}
    target:
      entity_id: input_boolean.wled_desk_led_state
  description: Control WLED on the desk led
```

</details>

<details>
  <summary>script 3 - effects</summary>
  
```
wled_desk_led_effect:
  alias: wled desk led effect
  sequence:
  - data:
      entity_id: input_select.wled_desk_led_effect
      option: '{{ effect }}'
    action: input_select.select_option
  - data:
      'on': 1
      brightness: '{{ states(''input_number.wled_desk_led_brightness'') | int }}'
      red: '{{ states(''input_number.wled_desk_led_red'') | int }}'
      green: '{{ states(''input_number.wled_desk_led_green'') | int }}'
      blue: '{{ states(''input_number.wled_desk_led_blue'') | int }}'
      effect: '
        {% set effect = states(''input_select.wled_desk_led_effect'') %}
        {% if effect == ''Solid'' %}0
        {% elif effect == ''Blink'' %}1
        {% elif effect == ''Breathe'' %}2
        {% elif effect == ''Wipe'' %}3
        {% elif effect == ''Wipe Random'' %}4
        {% elif effect == ''Random Colors'' %}5
        {% elif effect == ''Sweep'' %}6
        {% elif effect == ''Dynamic'' %}7
        {% elif effect == ''Colorloop'' %}8
        {% elif effect == ''Rainbow'' %}9
        {% elif effect == ''Scan'' %}10
        {% elif effect == ''Scan Dual'' %}11
        {% elif effect == ''Fade'' %}12
        {% elif effect == ''Theater'' %}13
        {% elif effect == ''Theater Rainbow'' %}14
        {% elif effect == ''Running'' %}15
        {% elif effect == ''Saw'' %}16
        {% elif effect == ''Twinkle'' %}17
        {% elif effect == ''Dissolve'' %}18
        {% elif effect == ''Dissolve Rnd'' %}19
        {% elif effect == ''Sparkle'' %}20
        {% elif effect == ''Sparkle Dark'' %}21
        {% elif effect == ''Sparkle+'' %}22
        {% elif effect == ''Strobe'' %}23
        {% elif effect == ''Strobe Rainbow'' %}24
        {% elif effect == ''Strobe Mega'' %}25
        {% elif effect == ''Blink Rainbow'' %}26
        {% elif effect == ''Android'' %}27
        {% elif effect == ''Chase'' %}28
        {% elif effect == ''Chase Random'' %}29
        {% elif effect == ''Chase Rainbow'' %}30
        {% elif effect == ''Chase Flash'' %}31
        {% elif effect == ''Chase Flash Rnd'' %}32
        {% elif effect == ''Rainbow Runner'' %}33
        {% elif effect == ''Colorful'' %}34
        {% elif effect == ''Traffic Light'' %}35
        {% elif effect == ''Sweep Random'' %}36
        {% elif effect == ''Chase 2'' %}37
        {% elif effect == ''Aurora'' %}38
        {% elif effect == ''Stream'' %}39
        {% elif effect == ''Scanner'' %}40
        {% elif effect == ''Lighthouse'' %}41
        {% elif effect == ''Fireworks'' %}42
        {% elif effect == ''Rain'' %}43
        {% elif effect == ''Tetrix'' %}44
        {% elif effect == ''Fire Flicker'' %}45
        {% elif effect == ''Gradient'' %}46
        {% elif effect == ''Loading'' %}47
        {% elif effect == ''Fairy'' %}49
        {% elif effect == ''Two Dots'' %}50
        {% elif effect == ''Fairytwinkle'' %}51
        {% elif effect == ''Running Dual'' %}52
        {% elif effect == ''Chase 3'' %}54
        {% elif effect == ''Tri Wipe'' %}55
        {% elif effect == ''Tri Fade'' %}56
        {% elif effect == ''Lightning'' %}57
        {% elif effect == ''ICU'' %}58
        {% elif effect == ''Multi Comet'' %}59
        {% elif effect == ''Scanner Dual'' %}60
        {% elif effect == ''Stream 2'' %}61
        {% elif effect == ''Oscillate'' %}62
        {% elif effect == ''Pride 2012'' %}63
        {% elif effect == ''Juggle'' %}64
        {% elif effect == ''Palette'' %}65
        {% elif effect == ''Fire 2012'' %}66
        {% elif effect == ''Colorwaves'' %}67
        {% elif effect == ''Bpm'' %}68
        {% elif effect == ''Fill Noise'' %}69
        {% elif effect == ''Noise 1'' %}70
        {% elif effect == ''Noise 2'' %}71
        {% elif effect == ''Noise 3'' %}72
        {% elif effect == ''Noise 4'' %}73
        {% elif effect == ''Colortwinkles'' %}74
        {% elif effect == ''Lake'' %}75
        {% elif effect == ''Meteor'' %}76
        {% elif effect == ''Meteor Smooth'' %}77
        {% elif effect == ''Railway'' %}78
        {% elif effect == ''Ripple'' %}79
        {% elif effect == ''Twinklefox'' %}80
        {% elif effect == ''Twinklecat'' %}81
        {% elif effect == ''Halloween Eyes'' %}82
        {% elif effect == ''Solid Pattern'' %}83
        {% elif effect == ''Solid Pattern Tri'' %}84
        {% elif effect == ''Spots'' %}85
        {% elif effect == ''Spots Fade'' %}86
        {% elif effect == ''Glitter'' %}87
        {% elif effect == ''Candle'' %}88
        {% elif effect == ''Fireworks Starburst'' %}89
        {% elif effect == ''Fireworks 1D'' %}90
        {% elif effect == ''Bouncing Balls'' %}91
        {% elif effect == ''Sinelon'' %}92
        {% elif effect == ''Sinelon Dual'' %}93
        {% elif effect == ''Sinelon Rainbow'' %}94
        {% elif effect == ''Popcorn'' %}95
        {% elif effect == ''Drip'' %}96
        {% elif effect == ''Plasma'' %}97
        {% elif effect == ''Percent'' %}98
        {% elif effect == ''Ripple Rainbow'' %}99
        {% elif effect == ''Heartbeat'' %}100
        {% elif effect == ''Pacifica'' %}101
        {% elif effect == ''Candle Multi'' %}102
        {% elif effect == ''Solid Glitter'' %}103
        {% elif effect == ''Sunrise'' %}104
        {% elif effect == ''Phased'' %}105
        {% elif effect == ''Twinkleup'' %}106
        {% elif effect == ''Noise Pal'' %}107
        {% elif effect == ''Sine'' %}108
        {% elif effect == ''Phased Noise'' %}109
        {% elif effect == ''Flow'' %}110
        {% elif effect == ''Chunchun'' %}111
        {% elif effect == ''Dancing Shadows'' %}112
        {% elif effect == ''Washing Machine'' %}113
        {% elif effect == ''Candy Cane'' %}114
        {% elif effect == ''Blends'' %}115
        {% elif effect == ''TV Simulator'' %}116
        {% elif effect == ''Dynamic Smooth'' %}117
        {% else %}0
        {% endif %}
        '
    action: rest_command.wled_desk_led
  description: ''
```

</details>

## 5 - Create the following Helpers
We use those to save and retain the different states of the lights like: On, Off, Brightness, RGB colors values and last effect..

<details>
  <summary>Hellpers</summary>
  
```
input_boolean:
  wled_desk_led_state:
    name: WLED Desk Led State

input_number:
  wled_desk_led_brightness:
    name: WLED Desk Led Brightness
    min: 0
    max: 255
    step: 1

  wled_desk_led_red:
    name: WLED Desk Led Red
    min: 0
    max: 255
    step: 1

  wled_desk_led_green:
    name: WLED Desk Led Green
    min: 0
    max: 255
    step: 1

  wled_desk_led_blue:
    name: WLED Desk Led Blue
    min: 0
    max: 255
    step: 1

```

</details>

## 6 - We need one more helper for effects:
this one we will create as yaml as it will take so much time to create in the ui.

* add this to `input_select.yaml`

<details>
  <summary>effects List</summary>
  
```
wled_desk_led_effect:
  name: "WLED Desk Led Effect"
  options:
    - Solid
    - Blink
    - Breathe
    - Wipe
    - Wipe Random
    - Random Colors
    - Sweep
    - Dynamic
    - Colorloop
    - Rainbow
    - Scan
    - Scan Dual
    - Fade
    - Theater
    - Theater Rainbow
    - Running
    - Saw
    - Twinkle
    - Dissolve
    - Dissolve Rnd
    - Sparkle
    - Sparkle Dark
    - Sparkle+
    - Strobe
    - Strobe Rainbow
    - Strobe Mega
    - Blink Rainbow
    - Android
    - Chase
    - Chase Random
    - Chase Rainbow
    - Chase Flash
    - Chase Flash Rnd
    - Rainbow Runner
    - Colorful
    - Traffic Light
    - Sweep Random
    - Chase 2
    - Aurora
    - Stream
    - Scanner
    - Lighthouse
    - Fireworks
    - Rain
    - Tetrix
    - Fire Flicker
    - Gradient
    - Loading
    - Fairy
    - Two Dots
    - Fairytwinkle
    - Running Dual
    - Chase 3
    - Tri Wipe
    - Tri Fade
    - Lightning
    - ICU
    - Multi Comet
    - Scanner Dual
    - Stream 2
    - Oscillate
    - Pride 2012
    - Juggle
    - Palette
    - Fire 2012
    - Colorwaves
    - Bpm
    - Fill Noise
    - Noise 1
    - Noise 2
    - Noise 3
    - Noise 4
    - Colortwinkles
    - Lake
    - Meteor
    - Meteor Smooth
    - Railway
    - Ripple
    - Twinklefox
    - Twinklecat
    - Halloween Eyes
    - Solid Pattern
    - Solid Pattern Tri
    - Spots
    - Spots Fade
    - Glitter
    - Candle
    - Fireworks Starburst
    - Fireworks 1D
    - Bouncing Balls
    - Sinelon
    - Sinelon Dual
    - Sinelon Rainbow
    - Popcorn
    - Drip
    - Plasma
    - Percent
    - Ripple Rainbow
    - Heartbeat
    - Pacifica
    - Candle Multi
    - Solid Glitter
    - Sunrise
    - Phased
    - Twinkleup
    - Noise Pal
    - Sine
    - Phased Noise
    - Flow
    - Chunchun
    - Dancing Shadows
    - Washing Machine
    - Candy Cane
    - Blends
    - TV Simulator
    - Dynamic Smooth
  initial: Solid
  icon: mdi:palette
```
</details>

## 7 - Polling states from the controller (optional).
to make this method works as 2 way communication (changes using wled app/ui reflect to Home Assistant), we will implement http polling, which will let us poll the states of the controller every x time. In my case i set the interval at 5 seconds.

* add polling logic to your `sensors.yaml`
* replace controller ip address with yours.

<details>
  <summary>Polling logic</summary>
  
```
  - platform: rest
    name: "WLED Desk Poll"
    resource: "http://10.0.0.107/json/state"
    scan_interval: 5
    json_attributes:
      - on
      - bri
      - seg
    value_template: "{{ value_json.on }}"

  - platform: template
    sensors:
      wled_desk_poll_brightness:
        friendly_name: "WLED Desk Poll Brightness"
        value_template: "{{ state_attr('sensor.wled_desk_poll', 'bri') }}"
      
      wled_desk_poll_red:
        friendly_name: "WLED Desk Poll Red"
        value_template: "{{ state_attr('sensor.wled_desk_poll', 'seg')[0].col[0][0] }}"
      
      wled_desk_poll_green:
        friendly_name: "WLED Desk Poll Green"
        value_template: "{{ state_attr('sensor.wled_desk_poll', 'seg')[0].col[0][1] }}"
      
      wled_desk_poll_blue:
        friendly_name: "WLED Desk Poll Blue"
        value_template: "{{ state_attr('sensor.wled_desk_poll', 'seg')[0].col[0][2] }}"

      wled_desk_poll_current_effect:
        friendly_name: "WLED Desk Poll Current Effect"
        value_template: >
            {% set effects = [
              "Solid", "Blink", "Breathe", "Wipe", "Wipe Random", "Random Colors",
              "Sweep", "Dynamic", "Colorloop", "Rainbow", "Scan", "Scan Dual",
              "Fade", "Theater", "Theater Rainbow", "Running", "Saw", "Twinkle",
              "Dissolve", "Dissolve Rnd", "Sparkle", "Sparkle Dark", "Sparkle+",
              "Strobe", "Strobe Rainbow", "Strobe Mega", "Blink Rainbow",
              "Android", "Chase", "Chase Random", "Chase Rainbow", "Chase Flash",
              "Chase Flash Rnd", "Rainbow Runner", "Colorful", "Traffic Light",
              "Sweep Random", "Chase 2", "Aurora", "Stream", "Scanner", "Lighthouse",
              "Fireworks", "Rain", "Tetrix", "Fire Flicker", "Gradient", "Loading",
              "Fairy", "Two Dots", "Fairytwinkle", "Running Dual",
              "Chase 3", "Tri Wipe", "Tri Fade", "Lightning", "ICU", "Multi Comet",
              "Scanner Dual", "Stream 2", "Oscillate", "Pride 2012", "Juggle",
              "Palette", "Fire 2012", "Colorwaves", "Bpm", "Fill Noise", "Noise 1",
              "Noise 2", "Noise 3", "Noise 4", "Colortwinkles", "Lake", "Meteor",
              "Meteor Smooth", "Railway", "Ripple", "Twinklefox", "Twinklecat",
              "Halloween Eyes", "Solid Pattern", "Solid Pattern Tri", "Spots",
              "Spots Fade", "Glitter", "Candle", "Fireworks Starburst",
              "Fireworks 1D", "Bouncing Balls", "Sinelon", "Sinelon Dual",
              "Sinelon Rainbow", "Popcorn", "Drip", "Plasma", "Percent",
              "Ripple Rainbow", "Heartbeat", "Pacifica", "Candle Multi",
              "Solid Glitter", "Sunrise", "Phased", "Twinkleup", "Noise Pal",
              "Sine", "Phased Noise", "Flow", "Chunchun", "Dancing Shadows",
              "Washing Machine", "Candy Cane", "Blends", "TV Simulator",
              "Dynamic Smooth"
            ] %}
            {% set effect_id = state_attr('sensor.wled_desk_poll', 'seg')[0].fx %}
            {% if effect_id < effects | length %}
              {{ effects[effect_id] }}
            {% else %}
              "Solid"
            {% endif %}
```
</details>

<details>
  <summary>Automation to sync the light states with wled app</summary>
  
```
alias: WLED Desk Poll From App
description: ""
triggers:
  - entity_id:
      - sensor.wled_desk_poll
      - sensor.wled_desk_poll_brightness
      - sensor.wled_desk_poll_red
      - sensor.wled_desk_poll_green
      - sensor.wled_desk_poll_blue
      - sensor.wled_desk_poll_current_effect
    trigger: state
actions:
  - choose:
      - conditions:
          - condition: template
            value_template: "{{ is_state('sensor.wled_desk_poll', 'True') }}"
        sequence:
          - target:
              entity_id: input_boolean.wled_desk_led_state
            action: input_boolean.turn_on
            data: {}
      - conditions:
          - condition: template
            value_template: "{{ is_state('sensor.wled_desk_poll', 'False') }}"
        sequence:
          - target:
              entity_id: input_boolean.wled_desk_led_state
            action: input_boolean.turn_off
            data: {}
  - target:
      entity_id: input_number.wled_desk_led_brightness
    data:
      value: "{{ states('sensor.wled_desk_poll_brightness') | int }}"
    action: input_number.set_value
    enabled: true
  - target:
      entity_id: input_number.wled_desk_led_red
    data:
      value: "{{ states('sensor.wled_desk_poll_red') | int }}"
    action: input_number.set_value
  - target:
      entity_id: input_number.wled_desk_led_green
    data:
      value: "{{ states('sensor.wled_desk_poll_green') | int }}"
    action: input_number.set_value
  - target:
      entity_id: input_number.wled_desk_led_blue
    data:
      value: "{{ states('sensor.wled_desk_poll_blue') | int }}"
    action: input_number.set_value
  - target:
      entity_id: input_select.wled_desk_led_effect
    data:
      option: "{{ states('sensor.wled_desk_poll_current_effect') }}"
    action: input_select.select_option

```
</details>

Now Restart Home Assistant and find your new light, in my case `light.wled_desk_led`.

### Have Fun... and if you face any issue i will be happy to help if i got the time..

[latest_release]: https://github.com/Anashost/MY-HA-DASH/releases/latest

[releases_shield]: https://img.shields.io/github/release/Anashost/MY-HA-DASH.svg?style=popout

[releases]: https://github.com/Anashost/MY-HA-DASH/releases

[downloads_total_shield]: https://img.shields.io/github/downloads/Anashost/MY-HA-DASH/total

[community_forum_shield]: 
https://img.shields.io/badge/Fourms-23cede?style=for-the-badge&logo=HomeAssistant&logoColor=white

[community_forum]: https://community.home-assistant.io/t/wled-0-13-x-led-controller-home-assistant-revive/812940

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
