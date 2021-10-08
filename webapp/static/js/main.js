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
    },

    mounted: function() {
        hash = parseParms(document.location.hash.substring(1));
        if (hash.id_token) {
            this.token = hash.id_token;
            document.cookie = "mattiotToken=" + this.token + "; max-age=3600; path=/;";
        } else {
            this.token = getCookie("mattiotToken");
        }
     },

    methods: {
        authorize: function() {
            var url = config.authUrl + "?response_type=token&scope=openid&client_id=" + config.clientID + "&redirect_uri=" + config.calbackUrl;
            window.open(url, '_blank').focus(); 
        },

        sendLeds: async function () {
            this.isLoading = true;
            console.log("Sending Leds ", this.leds);
            try {
                const url = config.apiHost + "/cmd";
                let data = {
                    "msg_type": "led",
                    "msg_body": {
                        "leds": ["green", "yellow", "red"],
                        "status": [this.leds.green, this.leds.yellow, this.leds.red],
                    }
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
            } catch (error) {
                console.error('internal server error', error);
            }
            this.isLoading = false;
        },
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
