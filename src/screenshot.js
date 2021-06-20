targetElements = $('div.section.l-space_small');

screenshot(targetElements.eq(0)[0], 'screenshot_00.png');
screenshot(targetElements.eq(1)[0], 'screenshot_01.png');

function screenshot(targetElement, filename) {
    html2canvas(targetElement).then(canvas => {
        let downloadElement = document.createElement('a');
        downloadElement.href = canvas.toDataURL();
        downloadElement.download = filename;
        downloadElement.click();
    });
}
