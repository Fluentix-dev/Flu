import os
import subprocess
import customtkinter as ctk
import threading  # Import threading module

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class FluentixInstallerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Fluentix Installer / v0.0.1 Prerelease build")
        self.geometry("600x475")

        self.eula_acpt = False
        self.current_progress = 0.0
        self.progress_updating = True

        self.disp_eula()

    def change_appearance_mode_event(self, new_appearance_mode: str):
        """Change appearance mode."""
        ctk.set_appearance_mode(new_appearance_mode)

    def disp_eula(self):
        """Display the EULA acceptance screen."""
        self.cls_window()
        
        self.label = ctk.CTkLabel(
            self,
            text="Welcome to Fluentix!",
            font=("Segoe UI", 20),
            justify="center",
        )
        self.label.pack(pady=10)

        self.label = ctk.CTkLabel(
            self,
            text="Join our Discord server (fluentix.dev/discord) for news and updates!",
            font=("Segoe UI", 15),
            justify="center",
        )
        self.label.pack(pady=10)
        
        self.eula_tbox = ctk.CTkTextbox(
            self,
            width=560,
            height=200,
            wrap="none",
            font=("Consolas", 12),
        )
        self.eula_tbox.pack(pady=10, padx=10)
        self.eula_tbox.insert(
            "end",
            """Copyright (c) 2025 Fluentix

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.""",
        )
        self.eula_tbox.configure(state="disabled")

        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(
            self,
            values=["Light", "Dark", "System"],
            command=self.change_appearance_mode_event
        )
        self.appearance_mode_optionemenu.pack(pady=10)

        self.acp_var = ctk.BooleanVar()
        self.eula_checkbox = ctk.CTkCheckBox(
            self,
            text="I accept the license agreement.",
            variable=self.acp_var,
            onvalue=True,
            offvalue=False,
        )
        self.eula_checkbox.pack(pady=10)

        self.next_button = ctk.CTkButton(
            self,
            text="Next",
            command=self.on_next,
        )
        self.next_button.pack(pady=10)

    def on_next(self):
        """Handle the Next button click on the EULA screen."""
        if self.acp_var.get():
            self.eula_acpt = True
            self.inst_ui()
        else:
            self.eula_decl("You must accept the license agreement to proceed.")

    def inst_ui(self):
        """Display the installation UI."""
        self.cls_window()

        self.label = ctk.CTkLabel(
            self,
            text="Fluentix Installer",
            font=("Segoe UI", 20),
            justify="center",
        )
        self.label.pack(pady=20)

        self.instruction_label = ctk.CTkLabel(
            self,
            text="Click the button below to start installing Fluentix.",
            font=("Segoe UI", 14),
            justify="center",
        )
        self.instruction_label.pack(pady=10)

        self.install_button = ctk.CTkButton(
            self,
            text="Install Fluentix",
            command=self.start_inst,
        )
        self.install_button.pack(pady=20)

        self.console_output = ctk.CTkTextbox(
            self,
            width=560,
            height=200,
            wrap="none",
            font=("Consolas", 10),
        )
        self.console_output.pack(pady=10, padx=10)
        self.console_output.insert("end", "Ready to install Fluentix...\n")
        self.console_output.configure(state="disabled")

        self.progress_bar = ctk.CTkProgressBar(self, width=560)
        self.progress_bar.pack(pady=10, padx=10)
        self.progress_bar.set(0)

        self.current_progress = 0.0
        self.progress_updating = True

        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=("Segoe UI", 12),
            text_color="yellow",
        )
        self.status_label.pack(pady=10)

    def eula_decl(self, error_message):
        """Display an error message."""
        self.cls_window()

        self.error_label = ctk.CTkLabel(
            self,
            text=error_message,
            font=("Segoe UI", 14),
            text_color="red",
            justify="center",
        )
        self.error_label.pack(pady=20)

        self.back_button = ctk.CTkButton(
            self,
            text="Back",
            command=self.disp_eula,
        )
        self.back_button.pack(pady=20)

    def start_inst(self):
        """Start the Fluentix installation process in a separate thread."""
        self.install_button.configure(state="disabled")
        self.status_label.configure(text="Installing Fluentix... Please wait.")

        threading.Thread(target=self.run_inst_thread, daemon=True).start()
        
# multithreading part written by chatgpt cuz i am not skilled enough to do this lmfao
    
    def run_inst_thread(self):
        """Run the installation process in a separate thread."""
        try:
            self.run_installation_script()
            # Animate progress smoothly to 100% after all commands are finished.
            self.animate_progress_to(1)
            # Disable further progress updates and force progress bar to 100%.
            self.after(200, self.force_progress_bar_end)
            # Schedule UI updates in the main thread after successful installation.
            self.after(0, lambda: self.status_label.configure(
                text="Installation complete! Fluentix is ready to use.",
                text_color="green"
            ))
            self.after(0, self.update_to_exit_button)
        except Exception as e:
            # Schedule UI update in the main thread on failure.
            self.after(0, lambda: self.status_label.configure(
                text=f"Installation failed: {e}",
                text_color="red"
            ))
            self.after(0, lambda: self.install_button.configure(state="normal"))

    def update_to_exit_button(self):
        """Change the install button to an exit button after installation is complete."""
        self.install_button.configure(
            text="Exit",
            command=self.quit,  # Closes the application.
            state="normal"
        )

    def run_installation_script(self):
        """Execute the Fluentix installation process."""
        install_commands = [
            'curl -L -o fluentix.zip https://github.com/Fluentix-dev/Fluentix/archive/refs/heads/main.zip',
            'tar -xf fluentix.zip',
            'cd Fluentix-main && py setup.py install',
        ]

        total_steps = len(install_commands)
        step = 1

        for command in install_commands:
            self.log_to_console(f"Running: {command}\n")
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode != 0:
                self.log_to_console(f"Error: {result.stderr}\n", error=True)
                raise Exception(f"Error during installation: {result.stderr}")

            self.log_to_console(result.stdout)
            # Animate progress smoothly from the current progress to the new target value.
            target_progress = step / total_steps
            self.animate_progress_to(target_progress)
            step += 1

    def animate_progress_to(self, target):
        """
        Gradually animate the progress bar from its current value to the target value.
        Updates will only continue if self.progress_updating is True.
        """
        # If progress updates have been disabled, do nothing.
        if not self.progress_updating:
            return

        # If we're already close to the target, snap to it.
        if abs(self.current_progress - target) < 0.001:
            self.current_progress = target
            self.progress_bar.set(self.current_progress)
            return

        # Increase or decrease the progress by a fixed increment.
        if self.current_progress < target:
            self.current_progress += 0.01
            if self.current_progress > target:
                self.current_progress = target
        else:
            self.current_progress -= 0.01
            if self.current_progress < target:
                self.current_progress = target

        self.progress_bar.set(self.current_progress)
        # Schedule the next update after 10 milliseconds.
        self.after(10, lambda: self.animate_progress_to(target))

    def force_progress_bar_end(self):
        """Disable further updates and force the progress bar to 100%."""
        self.progress_updating = False  # Disable further progress updates.
        self.current_progress = 1.0
        self.progress_bar.set(1.0)

    def log_to_console(self, message, error=False):
        """Log a message to the console output box."""
        self.console_output.configure(state="normal")  # Enable editing to insert text.
        if error:
            message = f"[ERROR] {message}"
        self.console_output.insert("end", message)
        self.console_output.see("end")  # Scroll to the end.
        self.console_output.configure(state="disabled")  # Disable editing again.

    def cls_window(self):
        """Clear all widgets from the window."""
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = FluentixInstallerApp()
    app.mainloop()
