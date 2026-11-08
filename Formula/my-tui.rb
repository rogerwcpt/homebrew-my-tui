class MyTui < Formula
  desc "Terminal-first session orchestrator"
  homepage "https://github.com/rogerwcpt/weissdigital-my-tui"
  license "MIT"

  on_macos do
    on_arm do
      url "https://github.com/rogerwcpt/weissdigital-my-tui/releases/download/v0.1.3/my-tui-0.1.3-osx-arm64.tar.gz"
      sha256 "eddac59c15f6e6953ba198f70c2077043936f7ade25ac728201e1c9eb4982959"
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
