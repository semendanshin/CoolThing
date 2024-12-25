import Navbar from "./components/Navbar.tsx";
import {Route, Routes} from "react-router-dom";
import ViewPort from "./components/ViewPort.tsx";
import Bots from "./pages/Bots.tsx";
import Campaigns from "./pages/Campaigns.tsx";
import NotFound from "./pages/NotFound.tsx";
import GPTSettings from "./pages/GPTSettings.tsx";
import Chats from "./pages/Chats.tsx";
import UpdateBotPage from "./pages/Bot.tsx";
import GPTSetting from "./pages/GPTSetting.tsx";
import Campaign from "./pages/Campaign.tsx";
import {CampaignRepositoryProvider} from "./context/CampaignRepositoryContext.tsx";
import {GPTSettingRepositoryProvider} from "./context/GPTSettingRepositoryContext.tsx";

function App() {
    const items = [
        {title: "My Bots", link: "/bots"},
        {title: "Campaigns", link: "/campaigns"},
        {title: "GPT Settings", link: "/gpts"},
        {title: "Chats", link: "/chats"},
    ];

    return (
        <>
            <Navbar items={items}/>
            <ViewPort>
                <Routes>
                    {/*<Route path="/" element={Dashboard} />*/}
                    <Route path="/bots" element={<Bots/>}/>
                    <Route path="/bots/:id" element={<UpdateBotPage/>}/>
                    <Route path="/campaigns" element={
                        <CampaignRepositoryProvider>
                            <Campaigns/>
                        </CampaignRepositoryProvider>
                    }/>
                    <Route path="/campaigns/:id" element={
                        <CampaignRepositoryProvider>
                            <GPTSettingRepositoryProvider>
                                <Campaign/>
                            </GPTSettingRepositoryProvider>
                        </CampaignRepositoryProvider>
                    }/>
                    <Route path="/gpts" element={<GPTSettings/>}/>
                    <Route path="/gpts/:id" element={<GPTSetting/>}/>
                    <Route path="/chats" element={<Chats/>}/>
                    <Route path="*" element={<NotFound/>}/>
                </Routes>
            </ViewPort>
        </>
    )
}

export default App
