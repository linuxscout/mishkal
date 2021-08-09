# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(["interfaces\\web\\mishkal_bottle.py"],
             pathex=['D:\\projects\\mishkal'],
             binaries=[],
             datas=[("data/*","data"),
             ("maskouk/data/*","maskouk/data"),             
             # for web
('interfaces/web/resources/*','resources'),
('interfaces/web/resources/errorPages/*','resources/errorPages'),
('interfaces/web/resources/errorPages/images/*','resources/errorPages/images'),
('interfaces/web/resources/files/*','resources/files'),
('interfaces/web/resources/files/fonts/*','resources/files/fonts'),
('interfaces/web/resources/files/images/*','resources/files/images'),
('interfaces/web/resources/files/samples/*','resources/files/samples'),
('interfaces/web/resources/files/xzero-rtl/*','resources/files/xzero-rtl'),
('interfaces/web/resources/files/xzero-rtl/css/*','resources/files/xzero-rtl/css'),
('interfaces/web/resources/files/xzero-rtl/fonts/*','resources/files/xzero-rtl/fonts'),
('interfaces/web/resources/files/xzero-rtl/js/*','resources/files/xzero-rtl/js'),
('interfaces/web/resources/static/*','resources/static'),
('interfaces/web/resources/templates/*','resources/templates'),
('interfaces/web/views/*','views'),
('interfaces/web/tmp/*','tmp'),




             
             ],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts, 
          [],
          exclude_binaries=True,
          name='mishkal-web',
          debug=True,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='mishkal-web')
