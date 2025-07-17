import { ThemeToggle } from "./theme-toggle";

export const Header = () => {
  return (
    <>
      <header className="flex items-center justify-between px-2 sm:px-4 py-2 bg-background text-black dark:text-white w-full border-b">
        <div className="flex items-center space-x-3 sm:space-x-4">
          <ThemeToggle />
          <h1
  className="text-lg sm:text-xl font-bold"
  style={{ fontFamily: "'Be Vietnam Pro', sans-serif" }}
>
  🤖 Chatbot Tư Vấn Bệnh
</h1>

        </div>
      </header>
    </>
  );
};
