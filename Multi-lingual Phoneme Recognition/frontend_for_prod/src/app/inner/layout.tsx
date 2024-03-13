import AppBar from "@/components/AppBar";

export default function RootLayout({
    children,
  }: Readonly<{
    children: React.ReactNode;
  }>) {
    return (<>
            <AppBar/>
            {children} </>   );
  }
  