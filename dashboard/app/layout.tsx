import "./globals.css";
import ProtectedLayout from "../components/ProtectedLayout";

export const metadata = {
  title: "JobMatch MVP",
  description: "Admin dashboard for JobMatch MVP"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>
        <ProtectedLayout>{children}</ProtectedLayout>
      </body>
    </html>
  );
}
