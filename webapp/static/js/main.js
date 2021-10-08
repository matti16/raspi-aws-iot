var app = new Vue({
    el: '#app',
    data: {
        leds: {
            green: false,
            yellow: false,
            red: false,
        },
        responseMsg: "",
        isLoading: false,
        token: null,
        cameraImages: [],
        tab: "led",
    },

    mounted: function() {
        hash = parseParms(document.location.hash.substring(1));
        if (hash.id_token) {
            this.token = hash.id_token;
            document.cookie = "mattiotToken=" + this.token + "; max-age=3600; path=/;";
        } else {
            this.token = getCookie("mattiotToken");
        }

        if (this.token){
            this.getCameraImages();
        }

        if (hash.tab) {
            this.tab = hash.tab;
        }
     },

    methods: {
        authorize: function() {
            var url = config.authUrl + "?response_type=token&scope=openid&client_id=" + config.clientID + "&redirect_uri=" + config.calbackUrl;
            window.open(url, '_blank').focus(); 
        },

        sendCmd: async function(msg_type, msg_body) {
            this.isLoading = true;
            console.log("Sending ", msg_type);
            try {
                const url = config.apiHost + "/cmd";
                let data = {
                    "msg_type": msg_type,
                    "msg_body": msg_body
                };

                var headers = new Headers();
                headers.append("Content-Type", "application/json");
                headers.append("Authorization", this.token);
                var requestOptions = {
                    method: 'POST',
                    headers: headers,
                    body: JSON.stringify(data),
                    redirect: 'follow'
                };

                let response = await fetch(url, requestOptions);
                response = await response.text();
                console.log('Response', response);
                this.responseMsg = "Successfully sent";

            } catch (error) {
                console.error('internal server error', error);
                this.responseMsg = "An error occurred";
            }
            this.isLoading = false;
        },

        sendLeds: async function () {
            var body = {
                "leds": ["green", "yellow", "red"],
                "status": [this.leds.green, this.leds.yellow, this.leds.red],
            };
            this.sendCmd("led", body);
        },

        getCameraImages: async function() {
            this.isLoading = true;
            try {
                const url = config.apiHost + "/camera";
                var headers = new Headers();
                headers.append("Authorization", this.token);
                var requestOptions = {
                    method: 'GET',
                    headers: headers,
                    redirect: 'follow'
                };

                let response = await fetch(url, requestOptions);
                response = await response.text();
                console.log('Response', response);
                this.cameraImages = JSON.parse(response);
            } catch (error) {
                console.error('internal server error', error);
            }
            this.isLoading = false;
        },

        refreshCameraImages: async function () {
            await this.sendCmd("camera", null);
            this.isLoading = true;
            await new Promise(r => setTimeout(r, 5000));
            this.getCameraImages();
        }
    }
});

// Parses the URL parameters and returns an object
function parseParms(str) {
	var pieces = str.split("&"), data = {}, i, parts;
	for (i = 0; i < pieces.length; i++) {
		parts = pieces[i].split("=");
		if (parts.length < 2) {
			parts.push("");
		}
		data[decodeURIComponent(parts[0])] = decodeURIComponent(parts[1]);
	}
	return data;
};

function getCookie(cookieName) {
    let cookie = {};
    document.cookie.split(';').forEach(function(el) {
      let [key,value] = el.split('=');
      cookie[key.trim()] = value;
    })
    return cookie[cookieName];
};
