# Sripad Kilikar — Portfolio

## Publish on Netlify
1. Extract the ZIP.
2. In Netlify, deploy the extracted folder contents, keeping `index.html`, `_headers`, both résumé PDFs, and the `assets/` folder together.
3. Do not upload only `index.html`; the profile photo and brand logos use relative paths.

## Publish on GitHub Pages
1. Create a repository (for example, `sripad-portfolio`).
2. Upload the contents of this ZIP to the repository root (not the ZIP file itself).
3. Confirm `index.html`, both résumé PDFs, and the `assets/` folder are visible at the root.
4. In **Settings → Pages**, select **Deploy from a branch**, choose `main` and `/ (root)`, then Save.
5. Open the Pages URL after the build completes.

The profile photo is at `assets/DP.png`; brand logos are in the same `assets/` folder. Keep those paths unchanged. The résumé links are relative, so they work on Netlify and GitHub Pages project URLs.
