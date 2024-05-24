const form = document.querySelector('form');
const loader = document.querySelector('.pyramid-loader');
const amzLoader = document.getElementById('amz-loader');
const wrapper = document.querySelector('.wrapper')
const pos = document.querySelector('.positive');
const neg = document.querySelector('.negative');
const neu = document.querySelector('.neutral');
const unk = document.querySelector('.unknown');
const resContainer = document.querySelector('.results-container');
const amzForm = document.getElementById('amz-form');
const posRes = document.getElementById('pos-res');
const negRes = document.getElementById('neg-res');
const amzRes = document.querySelector('.amz-res');
const videoImg = document.querySelectorAll('.video-img');
const videoLink = document.querySelectorAll('.video-link');
const videoTitle = document.querySelectorAll('.video-title');
const ytError = document.querySelector('.yt-error');
const amzError = document.querySelector('.amz-error');
const radios = document.querySelectorAll('.radio-inputs input[type="radio"]');




form.addEventListener('submit', async (event) => {
    event.preventDefault();
    ytError.style.display = 'none';
    resContainer.style.display = 'none';
    loader.style.display = 'block';
    let url = form.elements['text'].value;
    let id = getYouTubeVideoID(url);

    if(!id){
        loader.style.display = 'none';
        ytError.style.display = 'block';
        console.error('Invalid YouTube URL');
        return;
    }
    const formData = new FormData();
    formData.append('url', url);
    formData.append('id', id);

    try {
        const response = await fetch('/submit_form', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            loader.style.display = 'none';
            let res = await response.json();
            total = +res[0] + +res[1] + +res[2] + +res[3];
            res = res.map(x => (x / total) * 100);
            console.log(res);
            console.log(total);
            displayResults(res);
        } else {
            loader.style.display = 'none';
            console.error('Form submission failed');
        }
    } catch (error) {
        console.error('Error submitting form:', error);
    }
});

amzForm.addEventListener('submit', async (event) => {
    event.preventDefault();
    amzError.style.display = 'none';
    amzRes.style.display = 'none';
    amzLoader.style.display = 'block';
    let url = amzForm.elements['text'].value;
    if(!isValidAmazonProductURL(url)){
        amzLoader.style.display = 'none';
        amzError.style.display = 'block';
        console.error('Invalid YouTube URL');
        return;
    }
    lang = getSelectedRadioSpanText();
    const formData = new FormData();
    formData.append('url', url);
    formData.append('lang', lang);

    try {
        const response = await fetch('/submit_amz_form', {
            method: 'POST',
            body: formData
        });

        if (response.ok) {
            amzLoader.style.display = 'none';
            langChecker(lang);
            amzRes.style.display = 'flex';
            let res = await response.json();
            let positives = res.positives;
            let negatives = res.negatives;
            let videos = res.videos;
            posRes.innerHTML = positives.join('<br>');
            negRes.innerHTML = negatives.join('<br>');
            videoImg.forEach((img, i) => img.src = videos[i].thumbnail);
            videoTitle.forEach((title, i) => title.innerHTML = videos[i].title);
            videoLink.forEach((link, i) => link.href = videos[i].link);
        } else {
            amzLoader.style.display = 'none';
            console.error('Form submission failed');
        }
    } catch (error) {
        console.error('Error submitting form:', error);
    }
});

function getYouTubeVideoID(url) {
    var regExp = /^.*((youtu.be\/)|(v\/)|(\/u\/\w\/)|(embed\/)|(watch\?)|(shorts\/))\??v?=?([^#\&\?]*).*/;
    var match = url.match(regExp);
    return (match && match[8].length == 11) ? match[8] : false;
}

function isValidAmazonProductURL(url) {
    var regExp = /\/(dp|gp\/product)\/([A-Z0-9]+)/i;
    return regExp.test(url);
}

function displayResults(res) {
    pos.setAttribute('per', (+res[0]).toFixed(2) + '%');
    neg.setAttribute('per', (+res[1]).toFixed(2) + '%');
    neu.setAttribute('per', (+res[2]).toFixed(2) + '%');
    unk.setAttribute('per', (+res[3]).toFixed(2) + '%');
    pos.style.maxWidth = pos.getAttribute('per');
    neg.style.maxWidth = neg.getAttribute('per');
    neu.style.maxWidth = neu.getAttribute('per');
    unk.style.maxWidth = unk.getAttribute('per');
    resContainer.style.display = 'block';
    window.getComputedStyle(resContainer).getPropertyValue("opacity"); // Trigger a reflow
    resContainer.classList.add('show');
}


// Get all radio inputs


// Function to get the selected radio's span text
function getSelectedRadioSpanText() {
    for (var i = 0; i < radios.length; i++) {
        if (radios[i].checked) {
            return radios[i].nextElementSibling.textContent;
        }
    }
}

function langChecker(lang){
    if (lang == 'French'){
        amzRes.children[0].innerHTML = 'Positifs';
        amzRes.children[2].innerHTML = 'Négatifs';
    } else if (lang == 'Arabic'){
        amzRes.children[0].innerHTML = 'إيجابيات';
        amzRes.children[2].innerHTML = 'سلبيات';
    }
}
