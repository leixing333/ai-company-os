import React from 'react';

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-gray-950 text-white">
      {/* Hero Section */}
      <section className="flex flex-col items-center py-24 px-6">
        <h1 className="text-5xl font-bold text-center max-w-3xl">
          AI 驱动的设计服务，交付速度提升 4 倍
        </h1>
        <p className="text-xl text-gray-400 mt-6 text-center max-w-xl">
          订阅即用，无需招聘，随时暂停
        </p>
        <div className="flex gap-4 mt-10">
          <button className="bg-blue-600 hover:bg-blue-500 px-8 py-4 rounded-xl font-semibold">
            查看方案
          </button>
          <button className="border border-gray-700 px-8 py-4 rounded-xl font-semibold">
            预约演示
          </button>
        </div>
      </section>
      {/* Pricing Section */}
      <section className="flex justify-center py-20 px-6">
        <div className="bg-gray-900 border border-gray-800 rounded-2xl p-10 max-w-md w-full">
          <div className="text-6xl font-bold">$999<span className="text-2xl text-gray-400">/月</span></div>
          <p className="text-gray-400 mt-2">一个请求，无限可能</p>
          <button className="w-full bg-blue-600 hover:bg-blue-500 py-4 rounded-xl font-semibold mt-8">
            立即订阅
          </button>
          <p className="text-gray-500 text-sm text-center mt-4">随时暂停或取消，无合同绑定</p>
        </div>
      </section>
    </div>
  );
};

export default LandingPage;
