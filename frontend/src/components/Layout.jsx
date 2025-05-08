import Header from './Header';
import Sidebar from './Sidebar';

function Layout({ children }) {
  return (
    <div className="flex h-screen">
      <Sidebar />
      <div className="flex flex-col flex-1 overflow-hidden">
        <Header />
        <main className="p-6 overflow-y-auto">{children}</main>
      </div>
    </div>
  );
}

export default Layout;
