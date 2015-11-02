from fxpt.fx_texture_manager.processors import ProcessorCopyMove


filesToProcess = [
    '',
    '%FXPT_LOCATION%/src/dirA/testTex_exit.png',
    '%INVALID_ENV_VAR%/fxpt/fx_texture_manager/icons/copy.png',
    '%INVALID_ENV_VAR%/fxpt/fx_texture_manager/icons/copy.png',
    '//BLACK/C$/__testTextureManager__/src/dirB/dirB1/retarget.png',
    '//BLACK/C$/__testTextureManager__/src/dirB/dirB1/retarget.png',
    '//BLACK/C$/__testTextureManager__/src/dirB/dirB1/retarget.png',
    'C:/GitHub/fxpt/fxpt/fx_texture_manager/tests/testMayaProject/sourceimages/testTex_exit.png',
]


if __name__ == '__main__':
    proc = ProcessorCopyMove(
        filenames=filesToProcess,
        targetRoot='C:/__test__',
        delSrc=False,
        copyFolderStruct=True,
        sourceRoot='',
        copyAdd=False,
        addSuffixes=''
    )

    proc.execute()
