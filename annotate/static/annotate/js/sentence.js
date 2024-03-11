function NextReviewLevel(sentenceId, currentLevel) {

    if (currentLevel >= 9) {
        console.log("Maximum review level reached.");
        return;
    }

    let hostname = location.hostname;

    const sentenceUrl = "https://" + hostname + ":8000/annotate/api_v1/sentence/" + String(sentenceId) + "/"
    const dataObject = {
        review_level: currentLevel + 1
    };

    fetch(sentenceUrl, {
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
