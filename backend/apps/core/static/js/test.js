
const selectedTags = new Set();
const selectedTagsContainer = document.getElementById('selectedTags');
const input = document.getElementById('tagInput');

function renderTags() {
    selectedTagsContainer.innerHTML = '';
    selectedTags.forEach(tag => {
        const tagEl = document.createElement('span');
        tagEl.className = 'bg-white text-green-500 border border-green-500 px-3 py-1 rounded-full text-sm flex items-center';
        tagEl.innerHTML = `${tag}
        <button class="ml-2 text-gray-500 hover:text-red-600" onclick="removeTag('${tag}')">&times;</button>`;
        selectedTagsContainer.appendChild(tagEl);
    });
}

function addTag(tag) {
    if (tag && !selectedTags.has(tag)) {
        selectedTags.add(tag);
        renderTags();
    }
}

function removeTag(tag) {
    selectedTags.delete(tag);
    renderTags();
}

input.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
        e.preventDefault();
        const tag = input.value.trim();
        if (tag) {
            addTag(tag);
            input.value = '';
        }
    }
});