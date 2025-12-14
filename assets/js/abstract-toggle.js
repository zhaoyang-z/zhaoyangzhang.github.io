function toggleAbstract(abstractId) {
    const abstract = document.getElementById('abstract-' + abstractId);
    if (abstract) {
        const isHidden = abstract.style.display === 'none' || abstract.style.display === '';
        abstract.style.display = isHidden ? 'block' : 'none';
    }
}