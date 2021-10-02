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
    },

    methods: {
        sendLeds: async function () {
            this.isLoading = true;
            console.log("Sending Leds ", this.leds);
            try {
                const url = config.apiHost;
                let data = {
                    "msg_type": "led",
                    "msg_body": {
                        "leds": ["green", "yellow", "red"],
                        "status": [this.leds.green, this.leds.yellow, this.leds.red],
                    }
                };

                var headers = new Headers();
                headers.append("Content-Type", "application/json");
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
        }
    }
});

console.log(config.apiHost);