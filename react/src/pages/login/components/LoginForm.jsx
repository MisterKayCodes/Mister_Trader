import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import Input from "../../../components/ui/Input";
import Button from "../../../components/ui/Button";
import { Checkbox } from "../../../components/ui/Checkbox";
import Icon from "../../../components/AppIcon";
import { login } from "../../../auth/auth";

const LoginForm = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    telegramUserId: "",
    pin: "",
    rememberMe: false, // optional, not used in backend
  });
  const [errors, setErrors] = useState({});
  const [isLoading, setIsLoading] = useState(false);
  const [loginError, setLoginError] = useState("");

  const validateForm = () => {
    const newErrors = {};

    if (!formData.telegramUserId) {
      newErrors.telegramUserId = "Telegram User ID is required";
    } else if (!/^\d+$/.test(formData.telegramUserId.trim())) {
      newErrors.telegramUserId = "Telegram User ID must be a number";
    }

    if (!formData.pin) {
      newErrors.pin = "PIN is required";
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: "",
      }));
    }
    if (loginError) {
      setLoginError("");
    }
  };

  const handleCheckboxChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      rememberMe: e.target.checked,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoginError("");

    if (!validateForm()) {
      return;
    }

    setIsLoading(true);

    try {
      await login({
        telegram_user_id: Number(formData.telegramUserId.trim()),
        pin: formData.pin,
      });
      setIsLoading(false);
      navigate("/dashboard");
    } catch (error) {
      setLoginError(error.message || "Invalid Telegram User ID or PIN");
      setIsLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full space-y-6" noValidate>
      {loginError && (
        <div className="p-4 rounded-lg bg-destructive/10 border border-destructive/20 flex items-start gap-3">
          <Icon name="AlertCircle" size={20} className="text-destructive flex-shrink-0 mt-0.5" />
          <p className="text-sm text-destructive">{loginError}</p>
        </div>
      )}

      <Input
        type="text"
        name="telegramUserId"
        label="Telegram User ID"
        placeholder="Enter your Telegram user ID"
        value={formData.telegramUserId}
        onChange={handleInputChange}
        error={errors.telegramUserId}
        required
        disabled={isLoading}
      />

      <Input
        type="password"
        name="pin"
        label="PIN"
        placeholder="Enter your PIN"
        value={formData.pin}
        onChange={handleInputChange}
        error={errors.pin}
        required
        disabled={isLoading}
      />

      <div className="flex items-center justify-between">
        <Checkbox
          label="Remember me"
          checked={formData.rememberMe}
          onChange={handleCheckboxChange}
          disabled={isLoading}
        />
        <button
          type="button"
          className="text-sm font-medium text-primary hover:text-primary/80 transition-smooth focus-ring rounded px-2 py-1"
          disabled={isLoading}
          // You can add forgot PIN handler here if you want
        >
          Forgot PIN?
        </button>
      </div>

      <Button type="submit" variant="default" fullWidth loading={isLoading} disabled={isLoading}>
        {isLoading ? "Signing in..." : "Login"}
      </Button>
    </form>
  );
};

export default LoginForm;
