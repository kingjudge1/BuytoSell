import { useState } from 'react';
import { Button } from "/components/ui/button";
import { Input } from "/components/ui/input";
import { Label } from "/components/ui/label";
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "/components/ui/select";
import { toast } from "/components/ui/use-toast";
import { Check, Mail, FileText, ArrowLeft, Globe, Phone, Download, Clock, X } from 'lucide-react';
import { Tabs, TabsContent, TabsList, TabsTrigger } from "/components/ui/tabs";

// Nigerian states list
const nigerianStates = [
  "Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", 
  "Benue", "Borno", "Cross River", "Delta", "Ebonyi", "Edo", 
  "Ekiti", "Enugu", "FCT - Abuja", "Gombe", "Imo", "Jigawa", 
  "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara", 
  "Lagos", "Nasarawa", "Niger", "Ogun", "Ondo", "Osun", 
  "Oyo", "Plateau", "Rivers", "Sokoto", "Taraba", "Yobe", 
  "Zamfara", "Other"
];

// Trade percentage options
const tradePercentages = [
  "10%", "15%", "20%", "25%", "30%", "35%", "40%", "45%", "50%"
];

// Email status types
type EmailStatus = 'idle' | 'pending' | 'delivered' | 'failed';

// Type for transaction data
interface Transaction {
  id: string;
  fullName: string;
  state: string;
  date: string;
  amount: string;
  email: string;
  tradePercentage: string;
  pboName: string;
  timestamp: number;
  emailStatus: EmailStatus;
}

export default function PwanMaxLandApp() {
  const [activeTab, setActiveTab] = useState('form');
  const [formData, setFormData] = useState({
    fullName: '',
    state: '',
    date: new Date().toISOString().split('T')[0],
    amount: '',
    email: '',
    tradePercentage: '',
    pboName: ''
  });
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [selectedTransaction, setSelectedTransaction] = useState<Transaction | null>(null);
  const [receiptEmail, setReceiptEmail] = useState('');
  const [emailStatus, setEmailStatus] = useState<EmailStatus>('idle');
  const [analytics, setAnalytics] = useState({
    sent: 0,
    pending: 0,
    delivered: 0,
    failed: 0
  });

  // Play sound effects
  const playSound = (sound: 'success' | 'error' | 'notification') => {
    const sounds = {
      success: 'https://assets.mixkit.co/sfx/preview/mixkit-correct-answer-tone-2870.mp3',
      error: 'https://assets.mixkit.co/sfx/preview/mixkit-wrong-answer-fail-notification-946.mp3',
      notification: 'https://assets.mixkit.co/sfx/preview/mixkit-software-interface-start-2574.mp3'
    };
    const audio = new Audio(sounds[sound]);
    audio.play().catch(e => console.log('Audio play failed:', e));
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSelectChange = (name: string, value: string) => {
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validation
    if (!formData.fullName || !formData.state || !formData.amount || 
        !formData.email || !formData.tradePercentage || !formData.pboName) {
      alert('Please fill in all required fields');
      return;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(formData.email)) {
      alert('Please enter a valid email address');
      return;
    }

    if (isNaN(Number(formData.amount)) || Number(formData.amount) <= 0) {
      alert('Please enter a valid positive amount');
      return;
    }

    // Create new transaction
    const newTransaction: Transaction = {
      id: Date.now().toString(),
      ...formData,
      timestamp: Date.now(),
      emailStatus: 'idle'
    };

    // Save to transactions (simulating database)
    setTransactions(prev => [...prev, newTransaction]);
    setReceiptEmail(newTransaction.email); // Pre-fill receipt email

    // Play success sound
    playSound('success');

    // Show success toast
    toast({
      title: (
        <div className="flex items-center">
          <Check className="mr-2 h-4 w-4 text-green-500" />
          <span>Transaction Saved</span>
        </div>
      ),
      duration: 2000
    });

    // Reset form
    setFormData({
      fullName: '',
      state: '',
      date: new Date().toISOString().split('T')[0],
      amount: '',
      email: '',
      tradePercentage: '',
      pboName: ''
    });
  };

  const generateReceipt = (transaction: Transaction) => {
    setSelectedTransaction(transaction);
    setReceiptEmail(transaction.email);
    setActiveTab('receipt');
  };

  const downloadExcelReceipt = () => {
    if (!selectedTransaction) return;
    
    // Create CSV content
    const csvContent = [
      'PWAN MAX LAND BUY TO SELL - TRANSACTION RECEIPT',
      '',
      `Receipt ID:,${selectedTransaction.id}`,
      `Date:,${selectedTransaction.date}`,
      `Buyer Name:,${selectedTransaction.fullName}`,
      `PBO/Lead:,${selectedTransaction.pboName}`,
      `State:,${selectedTransaction.state}`,
      `Amount (₦):,₦${Number(selectedTransaction.amount).toLocaleString()}`,
      `Trade Percentage:,${selectedTransaction.tradePercentage}`,
      '',
      'Thank you for your investment in our Buy to Sell trade.',
      'Your money is growing and you are becoming more wealthy.'
    ].join('\n');

    // Create download link
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `PWAN-Receipt-${selectedTransaction.id}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);

    playSound('success');
    toast({
      title: (
        <div className="flex items-center">
          <Download className="mr-2 h-4 w-4 text-blue-500" />
          <span>Receipt Downloaded as CSV</span>
        </div>
      ),
      duration: 2000
    });
  };

  const sendReceipt = async () => {
    if (!selectedTransaction) return;
    
    // Validate email
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(receiptEmail)) {
      alert('Please enter a valid email address');
      return;
    }

    // Update status to pending
    setEmailStatus('pending');
    playSound('notification');
    updateTransactionStatus(selectedTransaction.id, 'pending');

    toast({
      title: (
        <div className="flex items-center">
          <Mail className="mr-2 h-4 w-4 text-yellow-500" />
          <span>Sending receipt to {receiptEmail}...</span>
        </div>
      ),
      duration: 2000
    });

    // Simulate email sending with delay
    try {
      await new Promise(resolve => setTimeout(resolve, 2000));
      
      // Randomly determine if email was delivered or failed (for demo purposes)
      const isSuccess = Math.random() > 0.2; // 80% success rate
      
      if (isSuccess) {
        setEmailStatus('delivered');
        playSound('success');
        updateTransactionStatus(selectedTransaction.id, 'delivered');
        
        toast({
          title: (
            <div className="flex items-center">
              <Check className="mr-2 h-4 w-4 text-green-500" />
              <span>Receipt delivered to {receiptEmail}</span>
            </div>
          ),
          duration: 3000
        });
      } else {
        setEmailStatus('failed');
        playSound('error');
        updateTransactionStatus(selectedTransaction.id, 'failed');
        
        toast({
          title: (
            <div className="flex items-center">
              <X className="mr-2 h-4 w-4 text-red-500" />
              <span>Failed to send to {receiptEmail}</span>
            </div>
          ),
          variant: 'destructive',
          duration: 3000
        });
      }
    } catch (error) {
      setEmailStatus('failed');
      playSound('error');
      updateTransactionStatus(selectedTransaction.id, 'failed');
      
      toast({
        title: (
          <div className="flex items-center">
            <X className="mr-2 h-4 w-4 text-red-500" />
            <span>Failed to send to {receiptEmail}</span>
          </div>
        ),
        variant: 'destructive',
        duration: 3000
      });
    }
  };

  const updateTransactionStatus = (id: string, status: EmailStatus) => {
    setTransactions(prev => 
      prev.map(tx => 
        tx.id === id ? { ...tx, emailStatus: status } : tx
      )
    );

    // Update analytics
    setAnalytics(prev => {
      const newAnalytics = { ...prev };
      if (status === 'delivered') newAnalytics.delivered++;
      if (status === 'pending') newAnalytics.pending++;
      if (status === 'failed') newAnalytics.failed++;
      newAnalytics.sent++;
      return newAnalytics;
    });
  };

  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="bg-gradient-to-r from-blue-600 to-red-600 text-white py-6 px-4 shadow-lg">
        <div className="container mx-auto text-center">
          <div className="flex justify-center mb-2">
            <div className="bg-white p-2 rounded-lg">
              <img 
                src="https://www.pwanmax.com/wp-content/uploads/2023/08/PWAN-MAX-LOGO.png" 
                alt="PWAN Max Logo" 
                className="h-16 object-contain"
                onError={(e) => {
                  const target = e.target as HTMLImageElement;
                  target.onerror = null;
                  target.src = '';
                  target.parentElement!.className = 'bg-gray-200 border-2 border-dashed rounded-xl w-16 h-16';
                }}
              />
            </div>
          </div>
          <h1 className="text-3xl font-bold">PWAN MAX LAND BUY TO SELL</h1>
          <p className="text-sm underline mt-1">Created by Judgewill Churchill</p>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8 max-w-6xl">
        <Tabs value={activeTab} onValueChange={setActiveTab}>
          <TabsList className="grid w-full grid-cols-4">
            <TabsTrigger value="form">Transaction Form</TabsTrigger>
            <TabsTrigger value="records">Transaction Records</TabsTrigger>
            <TabsTrigger value="receipt" disabled={!selectedTransaction}>
              Generate Receipt
            </TabsTrigger>
            <TabsTrigger value="analytics">Email Analytics</TabsTrigger>
          </TabsList>

          {/* Transaction Form Tab */}
          <TabsContent value="form">
            <form onSubmit={handleSubmit} className="space-y-6 mt-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                {/* Full Name */}
                <div>
                  <Label htmlFor="fullName">Full Name of Land Buyer</Label>
                  <Input
                    id="fullName"
                    name="fullName"
                    value={formData.fullName}
                    onChange={handleChange}
                    placeholder="Enter full name"
                    required
                  />
                </div>

                {/* PBO/Lead Name */}
                <div>
                  <Label htmlFor="pboName">Name of PBO/Lead</Label>
                  <Input
                    id="pboName"
                    name="pboName"
                    value={formData.pboName}
                    onChange={handleChange}
                    placeholder="Enter PBO/Lead name"
                    required
                  />
                </div>

                {/* State */}
                <div>
                  <Label htmlFor="state">State</Label>
                  <Select
                    value={formData.state}
                    onValueChange={(value) => handleSelectChange('state', value)}
                    required
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select state" />
                    </SelectTrigger>
                    <SelectContent>
                      {nigerianStates.map(state => (
                        <SelectItem key={state} value={state}>{state}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Date */}
                <div>
                  <Label htmlFor="date">Date of Deposit</Label>
                  <Input
                    id="date"
                    name="date"
                    type="date"
                    value={formData.date}
                    onChange={handleChange}
                    required
                  />
                </div>

                {/* Amount Deposited */}
                <div>
                  <Label htmlFor="amount">Amount Deposited (₦)</Label>
                  <Input
                    id="amount"
                    name="amount"
                    type="number"
                    value={formData.amount}
                    onChange={handleChange}
                    placeholder="Enter amount"
                    min="0"
                    step="0.01"
                    required
                  />
                </div>

                {/* Trade Percentage */}
                <div>
                  <Label htmlFor="tradePercentage">Trade Percentage</Label>
                  <Select
                    value={formData.tradePercentage}
                    onValueChange={(value) => handleSelectChange('tradePercentage', value)}
                    required
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Select percentage" />
                    </SelectTrigger>
                    <SelectContent>
                      {tradePercentages.map(percent => (
                        <SelectItem key={percent} value={percent}>{percent}</SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              {/* Email */}
              <div>
                <Label htmlFor="email">Gmail/Email</Label>
                <Input
                  id="email"
                  name="email"
                  type="email"
                  value={formData.email}
                  onChange={handleChange}
                  placeholder="Enter email"
                  required
                />
              </div>

              {/* Submit Button */}
              <div className="pt-4">
                <Button type="submit" className="w-full bg-gradient-to-r from-blue-600 to-red-600 hover:from-blue-700 hover:to-red-700">
                  Save Transaction
                </Button>
              </div>
            </form>
          </TabsContent>

          {/* Transaction Records Tab */}
          <TabsContent value="records">
            <div className="mt-6">
              {transactions.length === 0 ? (
                <div className="text-center py-8 text-gray-500">
                  No transactions recorded yet
                </div>
              ) : (
                <div className="overflow-x-auto">
                  <table className="min-w-full border">
                    <thead>
                      <tr className="bg-gray-100">
                        <th className="border p-2">Date</th>
                        <th className="border p-2">Buyer Name</th>
                        <th className="border p-2">PBO/Lead</th>
                        <th className="border p-2">State</th>
                        <th className="border p-2">Amount (₦)</th>
                        <th className="border p-2">Percentage</th>
                        <th className="border p-2">Email Status</th>
                        <th className="border p-2">Actions</th>
                      </tr>
                    </thead>
                    <tbody>
                      {transactions.map(tx => (
                        <tr key={tx.id} className="hover:bg-gray-50">
                          <td className="border p-2">{tx.date}</td>
                          <td className="border p-2">{tx.fullName}</td>
                          <td className="border p-2">{tx.pboName}</td>
                          <td className="border p-2">{tx.state}</td>
                          <td className="border p-2">₦{Number(tx.amount).toLocaleString()}</td>
                          <td className="border p-2">{tx.tradePercentage}</td>
                          <td className="border p-2">
                            <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                              tx.emailStatus === 'delivered' ? 'bg-green-100 text-green-800' :
                              tx.emailStatus === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                              tx.emailStatus === 'failed' ? 'bg-red-100 text-red-800' :
                              'bg-gray-100 text-gray-800'
                            }`}>
                              {tx.emailStatus === 'idle' ? 'Not Sent' : 
                               tx.emailStatus === 'pending' ? 'Pending' :
                               tx.emailStatus === 'delivered' ? 'Delivered' : 'Failed'}
                            </span>
                          </td>
                          <td className="border p-2">
                            <Button 
                              variant="outline" 
                              size="sm"
                              onClick={() => generateReceipt(tx)}
                              className="mr-2"
                            >
                              <FileText className="mr-2 h-4 w-4" />
                              Receipt
                            </Button>
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              )}
            </div>
          </TabsContent>

          {/* Receipt Generation Tab */}
          <TabsContent value="receipt">
            {selectedTransaction && (
              <div className="mt-6">
                <Button 
                  variant="outline" 
                  onClick={() => setActiveTab('records')}
                  className="mb-4"
                >
                  <ArrowLeft className="mr-2 h-4 w-4" />
                  Back to Records
                </Button>

                <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                  {/* Receipt Content */}
                  <div className="lg:col-span-2">
                    <div className="bg-white border rounded-lg p-6 shadow-sm mb-6">
                      <div className="flex justify-between items-center mb-6">
                        <div>
                          <img 
                            src="https://www.pwanmax.com/wp-content/uploads/2023/08/PWAN-MAX-LOGO.png" 
                            alt="PWAN Max Logo" 
                            className="h-16 object-contain"
                            onError={(e) => {
                              const target = e.target as HTMLImageElement;
                              target.onerror = null;
                              target.src = '';
                              target.className = 'bg-gray-200 border-2 border-dashed rounded-xl w-16 h-16';
                            }}
                          />
                        </div>
                        <div className="text-right">
                          <h2 className="text-xl font-bold">TRANSACTION RECEIPT</h2>
                          <p className="text-sm text-gray-500">Receipt #: {selectedTransaction.id}</p>
                        </div>
                      </div>

                      <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
                        <div>
                          <h3 className="font-semibold mb-2">Buyer Information</h3>
                          <p><span className="font-medium">Name:</span> {selectedTransaction.fullName}</p>
                          <p><span className="font-medium">State:</span> {selectedTransaction.state}</p>
                          <p><span className="font-medium">Email:</span> {selectedTransaction.email}</p>
                        </div>
                        <div>
                          <h3 className="font-semibold mb-2">Transaction Details</h3>
                          <p><span className="font-medium">Date:</span> {selectedTransaction.date}</p>
                          <p><span className="font-medium">Amount:</span> ₦{Number(selectedTransaction.amount).toLocaleString()}</p>
                          <p><span className="font-medium">Trade Percentage:</span> {selectedTransaction.tradePercentage}</p>
                          <p><span className="font-medium">PBO/Lead:</span> {selectedTransaction.pboName}</p>
                        </div>
                      </div>

                      <div className="bg-blue-50 border-l-4 border-blue-500 p-4 mb-6">
                        <p className="font-medium text-blue-800">
                          Thank you for your investment in our Buy to Sell trade. Your money is growing and you are becoming more wealthy.
                        </p>
                      </div>

                      <div className="border-t pt-4">
                        <p className="text-sm text-gray-500 mb-2">Thank you for your transaction with PWAN MAX</p>
                        <div className="flex justify-between items-center">
                          <div>
                            <p className="text-sm">System generated receipt</p>
                            <p className="text-xs text-gray-400">No signature required</p>
                          </div>
                        </div>
                      </div>
                    </div>

                    {/* Email Receipt Section */}
                    <div className="bg-white border rounded-lg p-6 shadow-sm">
                      <h3 className="font-semibold text-lg mb-4">Email Receipt</h3>
                      <div className="space-y-4">
                        <div>
                          <Label htmlFor="receiptEmail">Recipient Email</Label>
                          <Input
                            id="receiptEmail"
                            type="email"
                            value={receiptEmail}
                            onChange={(e) => setReceiptEmail(e.target.value)}
                            placeholder="Enter email to send receipt"
                          />
                        </div>
                        <div className="flex space-x-2">
                          <Button onClick={sendReceipt} className="flex-1">
                            <Mail className="mr-2 h-4 w-4" />
                            {emailStatus === 'pending' ? 'Sending...' : 'Send Receipt via Email'}
                          </Button>
                          <Button variant="outline" onClick={downloadExcelReceipt}>
                            <Download className="mr-2 h-4 w-4" />
                            Download CSV
                          </Button>
                        </div>
                        {emailStatus !== 'idle' && (
                          <div className={`p-3 rounded-md ${
                            emailStatus === 'delivered' ? 'bg-green-50 text-green-800' :
                            emailStatus === 'pending' ? 'bg-yellow-50 text-yellow-800' :
                            'bg-red-50 text-red-800'
                          }`}>
                            <div className="flex items-center">
                              {emailStatus === 'delivered' ? (
                                <Check className="mr-2 h-4 w-4" />
                              ) : emailStatus === 'pending' ? (
                                <Clock className="mr-2 h-4 w-4" />
                              ) : (
                                <X className="mr-2 h-4 w-4" />
                              )}
                              <span>
                                {emailStatus === 'delivered' ? 'Receipt successfully delivered' :
                                 emailStatus === 'pending' ? 'Receipt is being sent...' :
                                 'Failed to send receipt'}
                              </span>
                            </div>
                          </div>
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Contact Information */}
                  <div className="lg:col-span-1">
                    <div className="bg-gray-50 rounded-lg p-6 sticky top-4">
                      <h3 className="font-semibold text-lg mb-4">Contact Us</h3>
                      <div className="space-y-3">
                        <div className="flex items-center">
                          <Globe className="mr-2 h-5 w-5 text-blue-600" />
                          <a href="https://www.pwanmax.com" target="_blank" rel="noopener noreferrer" className="hover:underline">
                            www.pwanmax.com
                          </a>
                        </div>
                        <div className="flex items-center">
                          <Mail className="mr-2 h-5 w-5 text-red-600" />
                          <a href="mailto:pwanmaxtradeinfo@gmail.com" className="hover:underline">
                            pwanmaxtradeinfo@gmail.com
                          </a>
                        </div>
                        <div className="flex items-center">
                          <Phone className="mr-2 h-5 w-5 text-green-600" />
                          <a href="tel:08169945302" className="hover:underline">
                            08169945302
                          </a>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </TabsContent>

          {/* Analytics Tab */}
          <TabsContent value="analytics">
            <div className="mt-6">
              <h2 className="text-xl font-bold mb-4">Email Receipt Analytics</h2>
              
              <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
                <div className="bg-blue-50 border border-blue-100 rounded-lg p-4">
                  <h3 className="text-sm font-medium text-blue-800">Total Sent</h3>
                  <p className="text-2xl font-bold">{analytics.sent}</p>
                </div>
                <div className="bg-yellow-50 border border-yellow-100 rounded-lg p-4">
                  <h3 className="text-sm font-medium text-yellow-800">Pending</h3>
                  <p className="text-2xl font-bold">{analytics.pending}</p>
                </div>
                <div className="bg-green-50 border border-green-100 rounded-lg p-4">
                  <h3 className="text-sm font-medium text-green-800">Delivered</h3>
                  <p className="text-2xl font-bold">{analytics.delivered}</p>
                </div>
                <div className="bg-red-50 border border-red-100 rounded-lg p-4">
                  <h3 className="text-sm font-medium text-red-800">Failed</h3>
                  <p className="text-2xl font-bold">{analytics.failed}</p>
                </div>
              </div>

              {transactions.length > 0 ? (
                <div className="bg-white border rounded-lg p-6 shadow-sm">
                  <h3 className="font-medium mb-4">Recent Email Activities</h3>
                  <div className="overflow-x-auto">
                    <table className="min-w-full">
                      <thead>
                        <tr className="border-b">
                          <th className="text-left p-2">Receipt ID</th>
                          <th className="text-left p-2">Buyer</th>
                          <th className="text-left p-2">Amount</th>
                          <th className="text-left p-2">Status</th>
                          <th className="text-left p-2">Date</th>
                        </tr>
                      </thead>
                      <tbody>
                        {transactions
                          .filter(tx => tx.emailStatus !== 'idle')
                          .sort((a, b) => b.timestamp - a.timestamp)
                          .slice(0, 10)
                          .map(tx => (
                            <tr key={tx.id} className="border-b hover:bg-gray-50">
                              <td className="p-2">{tx.id}</td>
                              <td className="p-2">{tx.fullName}</td>
                              <td className="p-2">₦{Number(tx.amount).toLocaleString()}</td>
                              <td className="p-2">
                                <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                                  tx.emailStatus === 'delivered' ? 'bg-green-100 text-green-800' :
                                  tx.emailStatus === 'pending' ? 'bg-yellow-100 text-yellow-800' :
                                  'bg-red-100 text-red-800'
                                }`}>
                                  {tx.emailStatus === 'pending' ? 'Pending' :
                                   tx.emailStatus === 'delivered' ? 'Delivered' : 'Failed'}
                                </span>
                              </td>
                              <td className="p-2">{new Date(tx.timestamp).toLocaleString()}</td>
                            </tr>
                          ))}
                      </tbody>
                    </table>
                  </div>
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  No email activities recorded yet
                </div>
              )}
            </div>
          </TabsContent>
        </Tabs>
      </main>
    </div>
  );
}
