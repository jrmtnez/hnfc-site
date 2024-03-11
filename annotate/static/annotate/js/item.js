function ChangeSkipValidations(itemId, currValue) {

    let hostname = location.hostname; // ip of the current url, allows to use the same file for pre and pro

    const itemUrl = "https://" + hostname + ":8000/annotate/api_v1/item/" + String(itemId) + "/";
    const dataObject = {
        skip_validations: !currValue
    };

    fetch(itemUrl, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(dataObject)
    }).then(response => {
        location.reload(true);
        return response.json()
    }).then(data => {
        console.log(data)
    }).catch(rejected => {
        console.log(rejected);
    });
}

function DiscardItem(itemId) {

    let hostname = location.hostname; // ip of the current url, allows to use the same file for pre and pro

    const itemUrl = "https://" + hostname + ":8000/annotate/api_v1/item/" + String(itemId) + "/";
    const dataObject = {
        review_level: -1
    };

    fetch(itemUrl, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(dataObject)
    }).then(response => {
        location.reload(true);
        return response.json()
    }).then(data => {
        console.log(data)
    }).catch(rejected => {
        console.log(rejected);
    });
}
