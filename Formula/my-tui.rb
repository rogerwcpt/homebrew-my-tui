class MyTui < Formula
  desc "Terminal-first session orchestrator"
  homepage "https://github.com/rogerwcpt/weissdigital-my-tui"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/rogerwcpt/weissdigital-my-tui/releases/download/v0.1.9/my-tui-0.1.9-osx-arm64.tar.gz"
      sha256 "2d3d3375b78cb6f41e5bd9254585a9d59c2a3e571305febc2f79f37678898826"
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
