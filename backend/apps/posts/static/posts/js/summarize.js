

const target = document.querySelector('#id_summarize');

const observer = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            triggerSummarize();
            observer.unobserve(entry.target);
        }
    });
}, { threshold: 0.5 }); // Khi phần tử hiện ít nhất 50% trong viewport

observer.observe(target);

async function triggerSummarize() {
    const loadingEl = document.querySelector('#id_summarize_loading');
    loadingEl.classList.toggle('hidden');

    const data = target.dataset;

    const response = await fetch(data.url, {
        method: "POST",
        credentials: "include",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": window.csrfToken
        },
        body: JSON.stringify({
            post_id: data.post_id
        })
    });

    if (!response.ok) {
        const errorText = await response.text();
        console.error("Error response: ", errorText);
        return;
    }

    const result = await response.json();

    if (result.success) {

        const contentEL = document.querySelector('#id_summarize_content');
        typeWriterEffect(contentEL, result.content, 1);
        loadingEl.classList.toggle('hidden');

    } else {

        loadingEl.classList.toggle('hidden');
        console.error("Error: ", result.error);

    }
}

function typeWriterEffect(el, text, delay = 1) {
    el.textContent = '';
    let index = 0;

    function type() {
        if (index < text.length) {
            el.textContent += text.charAt(index);
            index++;
            setTimeout(type, delay);
        }
    }

    type();
}