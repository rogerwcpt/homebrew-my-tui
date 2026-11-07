class MyTui < Formula
  desc "Terminal-first session orchestrator"
  homepage "https://github.com/rogerwcpt/weissdigital-my-tui"
  version "0.1.0"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/rogerwcpt/weissdigital-my-tui/releases/download/v0.1.0/my-tui-0.1.0-osx-arm64.tar.gz"
      sha256 "bafdcc58594a9817152b0063fbaf36fe491b3d9be1ec522d8f3b9edbd039134c"
    end
  end

  def install
    # libmytui_pty.dylib has to stay beside the real binary. The symlink in
    # bin resolves to this libexec copy, which is the folder my-tui searches.
    libexec.install "my-tui", "libmytui_pty.dylib"
    bin.install_symlink libexec/"my-tui"
  end

  test do
    assert_predicate bin/"my-tui", :executable?
    assert_path_exists libexec/"libmytui_pty.dylib"
  end
end
