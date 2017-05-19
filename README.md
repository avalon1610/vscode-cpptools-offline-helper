# vscode-cpptools-offline-helper
help fix cpptools dependency when offline installing

VSCode Offline VSIX Download:
https://ms-vscode.gallery.vsassets.io/_apis/public/gallery/publisher/ms-vscode/extension/cpptools/ **`[version]`** /assetbyname/Microsoft.VisualStudio.Services.VSIXPackage

- rename Microsoft.VisualStudio.Services.VSIXPackage to cpptools.vsix or something else.
- install it by Ctrl+Shift+P , install from vsix.
- After Install VSIX, run fix_dependency.py, follow the step (**Works only on Windows**)
