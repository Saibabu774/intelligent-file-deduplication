from pathlib import Path
from app.services.hashing import sha256_file
def test_same_content_same_hash(tmp_path):
 a=tmp_path/'one.txt'; b=tmp_path/'different-name.txt'; a.write_bytes(b'hello duplicate'); b.write_bytes(b'hello duplicate'); assert sha256_file(a)==sha256_file(b)
def test_different_content_different_hash(tmp_path):
 a=tmp_path/'a'; b=tmp_path/'b'; a.write_bytes(b'abc'); b.write_bytes(b'abd'); assert sha256_file(a)!=sha256_file(b)
