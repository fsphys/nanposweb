// Define constants
const interval = 1000; // in ms
const bufferSize = 8 * 1024;
const readCard = new Uint8Array([49, 49, 13]);

const filters = [
  { usbVendorId: 2520, usbProductId: 1056 }
];

const buttonConnect = document.getElementById('connectButton');
buttonConnect.addEventListener('click', connectToPort);

const waitingForCard = document.getElementById('waitingForCard');

let timer;

/**
 * Sets |port| to the currently selected port. If none is selected then the
 * user is prompted for one.
 */
async function getSelectedPort() {
    try {
        const serial = navigator.serial;
        port = await serial.requestPort({ filters });
    } catch (e) {
        console.log("Couldn't select port!");
    }
}

function stopTimer() {
    clearInterval(timer);
}

function writeArray(data) {
    const writer = port.writable.getWriter();
    writer.write(data);
    writer.releaseLock();
}

async function connectToPort() {
    await getSelectedPort();
    if (!port) {
        return;
    }

    const options = {
        baudRate: 9600,
        dataBits: 8,
        parity: "none",
        stopBits: 1,
        flowControl: 'none',
        bufferSize,
    };

    console.log(options);
    console.log("Trying to connect");

    try {
        await port.open(options);
        console.log('<CONNECTED>');
    } catch (e) {
        console.error(e);
        if (e instanceof Error) {
            console.log(`<ERROR: ${e.message}>`);
        }
        console.log('<DISCONNECTED>');
        return;
    }

    // Toggle CSS
    buttonConnect.classList.toggle("hidden", true); // Hide the connect button
    waitingForCard.classList.toggle("hidden", false); // Show a message

    timer = setInterval(writeArray, interval, readCard);

    while (port && port.readable) {
        try {
            try {
                reader = port.readable.getReader();
            } catch {
                console.log("Couldn't create reader!")
                return;
            }

            let buffer = null;
            for (; ;) {
                const {value, done} = await (async () => {
                    return await reader.read();
                })();

                if (value) {
                    let input = String.fromCharCode.apply(null, value);
                    // Check the length of the string
                    if (input.length === 39) {
                        let items = input.split(";");
                        // Set the values
                        document.getElementById("card").setAttribute("value", items[0]);
                        document.getElementById("reader").setAttribute("value", items[1]);

                        // Submit the form
                        document.getElementById("cardForm").submit();
                    }
                }
                if (done) {
                    break;
                }
            }
        } catch (e) {
            console.error(e);
        } finally {
            if (reader) {
                reader.releaseLock();
                reader = undefined;
            }
        }
    }

    if (port) {
        try {
            await port.close();
        } catch (e) {
            console.error(e);
            if (e instanceof Error) {
                console.log(e.message);
            }
        }

    }
}